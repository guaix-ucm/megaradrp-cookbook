"""Upload the PDF of the cookbook as a new version of its Zenodo record.

The new version inherits the metadata of the latest published version;
only the version, the publication date and the file change.

The token is read from the environment variable ZENODO_TOKEN and needs
the scopes deposit:write and deposit:actions.

Without --publish the new version is left as a draft, to be reviewed
(and published or discarded) in the web interface of Zenodo.
"""

import argparse
import datetime
import os
import pathlib
import sys

import requests

API = {
    "zenodo": "https://zenodo.org/api",
    "sandbox": "https://sandbox.zenodo.org/api",
}

# Metadata fields of the previous version that must not be sent back
DROP_FIELDS = ("doi", "prereserve_doi")


def check(resp, what):
    if not resp.ok:
        sys.exit(f"error: {what}: HTTP {resp.status_code}\n{resp.text}")
    return resp


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", type=pathlib.Path, help="PDF file to upload")
    parser.add_argument("--record", required=True, help="id of any published version of the Zenodo record")
    parser.add_argument("--version", required=True, help="version of the new release, e.g. 2026.11.26")
    parser.add_argument("--date", default=datetime.date.today().isoformat(), help="publication date (default: today)")
    parser.add_argument("--server", choices=API, default="zenodo")
    parser.add_argument("--publish", action="store_true", help="publish the new version (default: leave a draft)")
    args = parser.parse_args()

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        sys.exit("error: ZENODO_TOKEN is not defined")
    if not args.pdf.is_file():
        sys.exit(f"error: {args.pdf} not found")

    api = API[args.server]
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"

    # Latest published version of the record
    resp = check(session.get(f"{api}/records/{args.record}/versions/latest"), "resolving the latest version")
    latest = resp.json()
    latest_version = latest["metadata"].get("version")
    print(f"latest version: {latest['id']} ({latest_version})")
    if latest_version == args.version:
        sys.exit(f"error: version {args.version} is already published in Zenodo")

    # New version (a draft)
    resp = session.post(f"{api}/deposit/depositions/{latest['id']}/actions/newversion")
    if resp.status_code == 400 and "remove all files" in resp.text:
        # Zenodo refuses a new version while a draft with files is open
        sys.exit(
            "error: there is an unpublished draft of a new version in Zenodo;\n"
            "publish it or discard it in https://zenodo.org/me/uploads and run again"
        )
    check(resp, "creating the new version")
    links = resp.json()["links"]
    draft_url = links.get("latest_draft", links["self"])
    draft = check(session.get(draft_url), "reading the draft").json()
    print(f"draft: {draft['id']} {draft['links'].get('html', '')}")

    # Remove the files inherited from the previous version
    for f in draft.get("files", []):
        url = f.get("links", {}).get("self") or f"{api}/deposit/depositions/{draft['id']}/files/{f['id']}"
        check(session.delete(url), f"deleting inherited file {f.get('filename')}")
        print(f"deleted inherited file {f.get('filename')}")

    # Upload the PDF
    filename = f"megara-cookbook_v{args.version}.pdf"
    with args.pdf.open("rb") as fd:
        check(session.put(f"{draft['links']['bucket']}/{filename}", data=fd), "uploading the PDF")
    print(f"uploaded {filename}")

    # Update the metadata
    metadata = {k: v for k, v in draft["metadata"].items() if k not in DROP_FIELDS}
    metadata["version"] = args.version
    metadata["publication_date"] = args.date
    check(session.put(draft["links"]["self"], json={"metadata": metadata}), "updating the metadata")
    print(f"metadata updated: version {args.version}, date {args.date}")

    if args.publish:
        resp = check(session.post(draft["links"]["publish"]), "publishing")
        record = resp.json()
        print(f"published: {record['doi']} {record['links'].get('record_html') or record['links'].get('html')}")
    else:
        print("draft left unpublished; review it and publish it from the Zenodo web interface")


if __name__ == "__main__":
    main()
