# Tekken 8 data things

Simple repo to keep some messy code and scripts used to generate some data about Tekken 8

## Overview

This project extracts data on matches from Tekken 8's online replay feature. This data is saved for re-use and analysis in this repo. 

In previous investigations of this nature the repo owner has monitored and mimiced network calls made to the games server. Tekken however does not use HTTP so tools like fiddler or charles proxy are of no help here.

Instead they used cheat engine to pull the replay list from the games memory directly. Using a combination of cheat engine and autohotkey, they refreshed the replay list (sorted by new) every 3 minutes to obtain a large number of games. 

## Installation
> List any dependencies and provide instructions on how to install them.

If you are just interested in the data, then no dependencies are needed since the data is saved in `complete_JSONS_[date]`. 

Other wise 

## Usage
> Provide instructions on how to use the project, including how to run any scripts or notebooks.

**Extracting match data from Tekken 8** 
The lua script is used in cheat engine to extract the json to a file on disk. You should edit this to change the directory if you are using this.
Note that due to memory being overwritten less than hald of the files generated this way are usable. You want to look for files with filesize greater than 720KB.

## Data
> Describe the datasets used in the analysis, including their sources and any preprocessing steps performed.

The data is saved in `complete_JSONS_[date]`. Each json contains 999 games.
A data dictionary is contained in `enums.py`.

## Analysis
> Explain the methodology used for the analysis, including any algorithms or techniques implemented.

The python notebook is simply used to do some basic analysis and generate charts

## Results
> Summarize the key findings and insights obtained from the analysis.

Current version contained in `data_processing.ipynb`

## Future Work
> Discuss any potential future improvements or additional analyses that could be performed.

Potential ideas:
- [ ] automate reporting and data (saves time / effort) 
- [ ] canvas feedback from Reddit 
- [ ] use T8 steam id (1pOnlineId/ 2pOnlineId) to link rank data to hours played stats (manual/ steam api)
- [ ] more accessible formt. dashboard? project page?

## Contributing

We welcome contributions to improve this project! To contribute, please follow these guidelines:

### Issues

If you encounter any issues with the project or have suggestions for improvements, please open an issue on GitHub. Provide as much detail as possible, including steps to reproduce the issue if applicable.

### Feature Requests

If you have an idea for a new feature, feel free to open an issue to discuss it. We appreciate any feedback and ideas for enhancing the project.

### Pull Requests

We encourage contributions from the community! If you'd like to fix a bug, add a new feature, or make other improvements, please follow these steps:

1. Fork the repository and create your branch from `main`.
2. Make your changes and ensure the code is properly formatted.
3. Test your changes thoroughly.
4. Create a pull request, describing the changes you've made and the rationale behind them.
5. Await feedback and be prepared to address any requested changes.

### License

By contributing to this project, you agree to license your contributions under the [MIT license](https://opensource.org/license/mit).

Thank you for contributing to this project and helping to make it better for everyone!

