# EMI-linggle-search

## Getting Started

### Prerequisites

- Python 3.10.4 or later

- [**local-mapreduce**](https://github.com/d2207197/local-mapreduce)

  A tool that simulates MapReduce on local environment.

  ```
  # Install GNU Parallel
  $ brew install parallel

  # Download local-mapreduce
  $ git clone --depth 1 https://github.com/d2207197/local-mapreduce.git

  # Install into system by creating a symbolic link
  $ sudo ln -s `pwd`/local-mapreduce/lmr /usr/local/bin

  # Refresh PATH
  $ hash -r
  ```

  Test is installed successfully:

  ```bash
  lmr

  # should output:
  # Usage: /usr/local/bin/lmr [-k] <BLOCKSIZE> <NUM_HASHING_SEGS> <MAPPER> <REDUCER> <OUTPUT_DIR>
  ```

### Virtual Environment Setup

To ensure an isolated environment for dependencies, follow these steps:

1. **Create a virtual environment** (only needed the first time):

   ```bash
   python -m venv .env
   ```

2. **Activate the virtual environment**:
   ```bash
   source .env/bin/activate  # macOS/Linux
   .env\Scripts\activate     # Windows
   ```

### Installation

Once the virtual environment is activated, install the necessary dependencies and data:

1. **Install required libraries:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy model:**

   [**spaCy**](https://spacy.io/) is an NLP library used for tokenization and Part-of-Speech (PoS) tagging.

   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Download NLTK data**

   NLTK is an NLP library used for sentence segmentation.

   ```bash
   python -m nltk.downloader punkt_tab -d .env/nltk_data
   ```

<!-- USAGE EXAMPLES -->

## Usage

**Step 1 - Sentence Segmentation and PoS Tagging**

```bash
python linggle-core/linggle/process/pos_v2.py <INPUT_FILE> > <POS_FILE>
```

**Step 2 - Ngram count**

```bash
cd linggle-core/linggle/process/
cat <POS_FILE> | lmr 1m 2 'python ngramcount_map.py' 'python ngramcount_reduce.py' <NC_OUT_FOLDER>
```

**Step 3 - Expand all possible Linggle queries with each ngram**

```bash
cd linggle-core/linggle/process/
cat <NC_OUT_FOLDER>/* | lmr 1m 2 'python ngramcount_map.py' 'python ngramcount_reduce.py' <LINGGLE_OUT_FOLDER>
```

**Step 4 - Load into database**

Before proceeding, ensure you **modify any hard-coded paths in the code** as needed.

Run the following script to load data into the database:

`linggle-core/linggle/database/emi_sqlite.py`

**Testing on Local CLI**

Once the database is generated, you can test it in the CLI using the following commands.

```bash
cd linggle-core
python -m linggle.database.emi
```
