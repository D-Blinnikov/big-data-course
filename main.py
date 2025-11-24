import os
from utils import run

ROOT = os.path.dirname(os.path.abspath(__file__))
TEXT_DATA = os.path.join(ROOT, "text-data")

def main():
    run("python run-hadoop-cluster.py")

    os.chdir(TEXT_DATA)
    run("python preprocess.py")

    os.chdir(ROOT)

    run("python run_step1_tf_df.py")

    run("python run_step2_tfidf.py")

    run("python search.py")


if __name__ == "__main__":
    main()
