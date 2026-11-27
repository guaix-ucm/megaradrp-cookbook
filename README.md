# MEGARADRP cookbook

Source code to generate the MEGARADRP Cookbook.

The corresponding web page is available at this
[link](https://guaix-ucm.github.io/megaradrp-cookbook/).

## PDF version

The PDF version is published in [Zenodo](https://doi.org/10.5281/zenodo.1974953)
by the workflow `generate-pdf`:

1. Update `release` in `cookbook/conf.py` (format `YYYY.MM.DD`) and merge it in `main`.
2. Create a GitHub release with a tag equal to `release`. The workflow builds
   the PDF, attaches it to the release and publishes it as a new version of
   the Zenodo record.

The workflow can also be run manually from the Actions tab, to build the PDF
only or to upload it to Zenodo as a draft (reviewed and published, or
discarded, in the web interface of Zenodo).

Zenodo does not create a new version while there is an unpublished draft
of a new version: publish it or discard it before running the workflow again.

The upload needs the repository secret `ZENODO_TOKEN`, a Zenodo personal
token of an owner of the record with the scopes `deposit:write` and
`deposit:actions`.
