from DrissionPage import ChromiumPage
import time
import json

dp = ChromiumPage()

url = "https://item.jd.com/100039640726.html#comment"
listen_url = 'api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc'
max_pages = 10
output_file = 'comments_data.json'
max_comments = 100

dp.listen.start(listen_url)
dp.get(url)
dp.scroll.to_bottom()
dp.ele("css:#detail > div.tab-main.large > ul > li:nth-child(5)").click()

unique_comments = set()
all_comments = []
total_comments = 0

try:
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page} ...")
        try:
            resp = dp.listen.wait()
            json_data = resp.response.body
            if not json_data:
                print("No valid data retrieved, skipping current page...")
                continue
            comments = json_data.get("comments", [])
            if not comments:
                print(f"No comments on page {page}, skipping...")
                continue
            for item in comments:
                if total_comments >= max_comments:
                    print(f"Scraped {max_comments} comments, stopping scraping.")
                    break
                content = item.get("content", "No content")
                if content in unique_comments:
                    continue
                unique_comments.add(content)
                creation_time = item.get("creationTime", "No time")
                location = item.get("location", "No location")
                print(f"Comment: {content}")
                print(f"Time: {creation_time}, Location: {location}")
                print("---------------")
                all_comments.append({
                    "content": content,
                    "creationTime": creation_time,
                    "location": location
                })
                total_comments += 1
            if total_comments >= max_comments:
                break
            dp.ele("css:.ui-pager-next").click()
            time.sleep(0.5)
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            break
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_comments, f, ensure_ascii=False, indent=4)
        print(f"Data successfully saved as {output_file}")
    except Exception as e:
        print(f"Error saving data: {e}")
finally:
    try:
        dp.quit()
        print("Browser exited, resources cleaned up.")
    except Exception as e:
        print(f"Error quitting browser: {e}")
    import gc
    gc.collect()

print("Scraping finished")
