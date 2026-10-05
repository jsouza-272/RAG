from src.cli_commands.cli_parsing import parse_dataset_path, parse_k, parse_max_chunk_size, parse_save_directory, parse_query


def test_paser_k():
    k = [1, 0, -1, 100, 1000.2, "sa", True, None]
    for n in k:
        try:
            print(parse_k(n))
        except Exception as error:
            print(f"\033[38;2;180;20;20m{error}\033[0m")


def test_parse_max_chunk_size():
    max_chunk_size = [1, -500, 500, 1000.2, 2000, 4000, "sa", True, None]
    for n in max_chunk_size:
        try:
            print(parse_max_chunk_size(n))
        except Exception as error:
            print(f"\033[38;2;180;20;20m{error}\033[0m")


def test_parse_dataset_path():
    dataset_path = ["", 1, True, None, 2.5, "t.json", "kjshad", "data/datasets_public/public/UnansweredQuestions",
                    #"data/datasets_public/public/UnansweredQuestions/dataset_code_public.json",
                    "data/datasets_public/public/UnansweredQuestions/dataset_docs_public.json"]
    for n in dataset_path:
        try:
            print(parse_dataset_path(n))
        except Exception as error:
            print(f"\033[38;2;180;20;20m{error}\033[0m")


def test_parse_save_directory():
    dataset_path = ["", 1, True, None, 2.5, "t.json", "kjshad", "test", "data/datasets_public/public/UnansweredQuestions", "data/datasets_public/public/UnansweredQuestions/dataset_code_public.json"]
    for n in dataset_path:
        try:
            print(parse_save_directory(n))
        except Exception as error:
            print(f"\033[38;2;180;20;20m{error}\033[0m")


def test_parse_query():
    query = ["", 1, True, None, 2.5, "     ", "-><>???//   /??!!  ", "___+_++_>>", "tjkashd", "1231313", "kljasd>>1io23ho1_+_"]
    for n in query:
        try:
            print(parse_query(n))
        except Exception as error:
            print(f"\033[38;2;180;20;20m{error}\033[0m")


test_parse_dataset_path()
