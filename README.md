# scan-reddit-for-vaporwave

Assumptions:
 - r/ImaginaryArchitecture has the fullname "t5_2x3v4", as fetched by the following API call:
 tests % ./test_execute_url.py "/search?q=ImaginaryArchitecture&type=sr"

Current State:
- The program authenticates, then fetches JSON data for the 100 newest images from the ImaginaryArchitecture subreddit. It uses the URLs from the returned JSON to download these 100 images to the temp directory.

Todos:
 - Use "before" and "after" logic (per the documentation "Listings do not use page numbers because their content changes so frequently," so this is a substitute for pagination) and count to get arbitrary numbers of images at a time to sort through. We can likely continue to exploit the NEW api call using these parameters to get arbitrary numbers of links (up to 100) an arbitary number of times (https://www.reddit.com/dev/api/#GET_new).
 - Delete non-vaporwave images from the temp folder.
 - Keep track of the ids of images from previous runs so that the program does not cover ground it has already covered.
 - Implement Pandas to do big data operations more efficiently.
 - Use an API call to locate the appropriate subreddit (or subreddits plural). This will only be needed if expanding the program at some point in the future.
 - Horizontal stripe method looks most promising. Use output from compile_stats_for_ideal_vaporwave_images.py to determine best guide values, then test. Implement the check_for_vaporwave_codes function based on these values, using a config file to make values easy to switch out.
 - Verify that vaporwave images are indeed getting moved to Output (no files seem to have passed so far). "Fails" and "Passes" are still getting printed by the helper script, so this can help with testing.
