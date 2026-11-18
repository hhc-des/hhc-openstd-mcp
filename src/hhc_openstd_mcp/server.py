"""MCP server wrapping the OpenSTD_Spider CLI for national standard search, info, and download."""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

mcp = FastMCP(
    name="tiantian-openstd-mcp",
    instructions="Search, query metadata, and download PDFs from the Chinese National Standard Full-Text Public System (国家标准全文公开系统, openstd.samr.gov.cn).",
)


def _run_openstd(*args: str) -> str:
    """Run openstd_spider CLI and return stdout."""
    cmd = ["openstd_spider", *args]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"openstd_spider {args[0]} failed (exit {result.returncode}): {result.stderr.strip()}")
    return result.stdout


@mcp.tool()
def search_standards(
    keyword: str = "",
    status: Optional[str] = None,
    std_type: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> str:
    """Search the Chinese National Standard Full-Text Public System (国家标准全文公开系统).

    Args:
        keyword: Search keyword (e.g., "通信管道", "综合布线", "GB 50374"). Can be a standard number or topic.
        status: Filter by status: "现行" (current), "即将实施" (upcoming), "废止" (abolished). None for all.
        std_type: Filter by standard type: "GB" (mandatory), "GBT" (recommended), "GBZ" (guiding). None for all.
        page: Page number (1-based).
        page_size: Results per page (10-50, default 20).

    Returns:
        JSON string with matched standards list (standard number, name, status, type, date, classification).
    """
    args = ["search", "--json", "-p", str(page), "--ps", str(page_size)]
    if keyword:
        args.append(keyword)
    if status:
        args += ["--status", status]
    if std_type:
        args += ["--type", std_type]

    output = _run_openstd(*args)
    return output


@mcp.tool()
def get_standard_info(target: str) -> str:
    """Query detailed metadata for a specific national standard.

    Args:
        target: Standard number (e.g., "GB 18030-2022") or the full URL of the standard page.

    Returns:
        JSON string with standard metadata: number, Chinese/English names, classification,
        publication date, implementation date, responsible body, etc.
    """
    args = ["info", "--json", target]
    output = _run_openstd(*args)
    return output


@mcp.tool()
def download_standard_pdf(target: str, output_dir: Optional[str] = None, preview: bool = False) -> str:
    """Download a national standard as PDF file.

    Args:
        target: Standard number (e.g., "GB 18030-2022") or the full URL of the standard page.
        output_dir: Directory to save the PDF (defaults to current working directory).
        preview: If True, force preview-mode download (for standards that only allow preview).

    Returns:
        Path to the downloaded PDF file.
    """
    args = ["download", target]
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        args += ["-o", output_dir]
    if preview:
        args.append("--preview")

    result = subprocess.run(
        ["openstd_spider"] + args,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Download failed: {result.stderr.strip()[:500]}")
    return result.stdout.strip()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
