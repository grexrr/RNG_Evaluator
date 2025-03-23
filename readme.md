# 📌 Prerequisite: Ensure config files exist in ./config/
# Each .cfg file should include:
#   - seed = <int>
#   - samples = <int>
#   - one or more distribution lines, e.g.:
#       dag a b p       # Dagum distribution
#       ske mu1 mu2     # Skellam distribution

# Manual
## Step 1: Generate samples from a specific config file
python generator.py config/your_file.cfg --output csv_data/your_file.csv

## Step 2: Generate plots from a generated CSV file
python plotter.py csv_data/your_file.csv --outdir pdf_graph

# Pipeline
## Run full pipeline (process all .cfg files in config/)
python driver.py --cfgdir config --csvdir csv_data --plotdir pdf_graph
