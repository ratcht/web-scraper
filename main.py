from concurrent.futures.thread import ThreadPoolExecutor
import concurrent.futures
import files.decorators as decorators



@decorators.time_to_execute
def main():
  executor = ThreadPoolExecutor(max_workers=10)

  items = ["Wedding Ring", "Wine Glass", "Face Cream"]
  futures = [executor.submit(scraper, item_name) for item_name in items]
  done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

  print(done)

  for task in done:
    print(task.result())