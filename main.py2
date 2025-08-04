from DrissionPage import ChromiumPage
import time
import json
import gc

class JDCommentScraper:
    def __init__(self, url, listen_url, max_pages=10, max_comments=100, output_file='comments_data.json'):
        self.url = url
        self.listen_url = listen_url
        self.max_pages = max_pages
        self.max_comments = max_comments
        self.output_file = output_file
        self.dp = ChromiumPage()
        self.all_comments = []
        self.unique_comments = set()
        self.total_comments = 0

    def _setup_browser_and_navigate(self):
        print("Setting up browser and navigating to comments section...")
        self.dp.listen.start(self.listen_url)
        self.dp.get(self.url)
        self.dp.scroll.to_bottom()
        self.dp.ele("css:#detail > div.tab-main.large > ul > li:nth-child(5)").click()

    def _process_comments(self, comments):
        for item in comments:
            if self.total_comments >= self.max_comments:
                return True
            content = item.get("content", "No content")
            if content in self.unique_comments:
                continue

            self.unique_comments.add(content)
            creation_time = item.get("creationTime", "No time")
            location = item.get("location", "No location")

            print(f"Comment: {content}")
            print(f"Time: {creation_time}, Location: {location}")
            print("---------------")

            self.all_comments.append({
                "content": content,
                "creationTime": creation_time,
                "location": location
            })
            self.total_comments += 1
        return self.total_comments >= self.max_comments

    def _save_to_json(self):
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_comments, f, ensure_ascii=False, indent=4)
            print(f"Data successfully saved as {self.output_file}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def _cleanup(self):
        try:
            self.dp.quit()
            print("Browser exited, resources cleaned up.")
        except Exception as e:
            print(f"Error quitting browser: {e}")
        finally:
            gc.collect()

    def scrape(self):
        self._setup_browser_and_navigate()
        try:
            for page in range(1, self.max_pages + 1):
                print(f"Scraping page {page} ...")
                try:
                    resp = self.dp.listen.wait()
                    json_data = resp.response.body
                    if not json_data:
                        print("No valid data retrieved, skipping current page...")
                        continue

                    comments = json_data.get("comments", [])
                    if not comments:
                        print(f"No comments on page {page}, skipping...")
                        continue

                    if self._process_comments(comments):
                        print(f"Scraped {self.max_comments} comments, stopping scraping.")
                        break

                    self.dp.ele("css:.ui-pager-next").click()
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Error scraping page {page}: {e}")
                    break
            
            self._save_to_json()

        finally:
            self._cleanup()
            print("Scraping finished")


if __name__ == '__main__':
    product_url = "https://item.jd.com/100039640726.html#comment"
    api_listen_url = 'api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc'
    
    scraper = JDCommentScraper(
        url=product_url,
        listen_url=api_listen_url,
        max_pages=10,
        max_comments=100,
        output_file='comments_data_oop.json'
    )
    scraper.scrape()
