import typer
from typing import Optional
import csv
from rich import print
from rich.progress import track
from getpapers.utils import fetch_pubmed_ids, fetch_paper_details

app = typer.Typer()

@app.command()
def main(
    query: str,
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Output CSV filename"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output"),
):
    if debug:
        print(f"[bold cyan]Fetching papers for query:[/bold cyan] '{query}'")

    ids = fetch_pubmed_ids(query)
    if debug:
        print(f"[bold green]PubMed IDs fetched:[/bold green] {ids}")

    results = []
    for pmid in track(ids, description="Processing papers..."):
        paper = fetch_paper_details(pmid)
        if paper:
            results.append(paper)

    if not results:
        print("[red]No non-academic papers found.[/red]")
        raise typer.Exit()

    headers = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Authors",
        "Company Affiliations",
        "Corresponding Email"
    ]

    if file:
        with open(file, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(results)
        print(f"[green]Results written to {file}[/green]")
    else:
        writer = csv.DictWriter(typer.echo, fieldnames=headers)
        typer.echo(",".join(headers))
        for row in results:
            typer.echo(",".join([row[h] for h in headers]))
