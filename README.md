# Tekken 8 data things

Simple repo to keep some messy code and scripts used to generate some data about Tekken 8

## Overview

This project extracts data on matches from Tekken 8's online replay feature. This data is saved for re-use and analysis in this repo. 

## Installation

If you are just interested in the data, please check my most recent reddit post which will always have a link to the data used for that post.

Otherwise, to gather data you can run data_download.ipynb to get data from the api at https://wank.wavu.wiki/api/

To run the python code for the data analysis and graph generation you simply need to install dependencies using [poetry](https://python-poetry.org/)

## Usage

Use data_download.ipynb to download data from https://wank.wavu.wiki/api/ and use data_processing.ipynb to calculate stats and graphs.

## Data

The data is downloaded to a series of files named `./output/matches_yyyy-mm-dd.json`. Each json contains the games for the specified date.
A dictionary which explains some of the mappings from the internal game variables to more readable forms is
available in `enums.py`.


## Analysis

The python notebook is simply used to do some basic analysis and generate charts. 
Mostly we want to look at rank distributions character play rates and character win rates.


## Future Work

Potential ideas:
- [ ] Store raw data in some online hosting service. Maybe just an S3 bucket.
- [ ] Generate more charts/analysis
    - [X] Per character rank distribution
    - [ ] Matchup table
    - [ ] Most popular secondary characters
    - [X] Some measure of "closeness of games" by looking at how many rounds are played in the average game
- [ ] Present data more accessible format. dashboard? project page?
- [ ] Use T8 steam id (1pOnlineId/ 2pOnlineId) to link rank data to hours played stats (manual/ steam api)

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

Using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) is encouraged.

### License

By contributing to this project, you agree to license your contributions under the [MIT license](https://opensource.org/license/mit).

Thank you for contributing to this project and helping to make it better for everyone!

