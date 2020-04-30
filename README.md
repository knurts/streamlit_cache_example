# streamlit_cache_example

1. Exhibit that a streamlit app can be run as a command with arguments, or as a web app.
```sh
    streamlit run cache_ex.py
    python3 cache_ex.py -b -i 1 -s abc -u peter
```
(I didn't try to perfect what's required, I think it may be better to assume web app first, and then attempt to parse for args.)

2. Exhibit that streamlit can run expensive functions at least once every run without being limited by a (ttl) time to live or (max_entries) number of cache entrie.
```sh
    Inspired by finding article by Rahul Agarwal, except his solution was still time based instead of the desired per run basis.
    Article:
    https://towardsdatascience.com/advanced-streamlit-caching-6f528a0f9993
    Code on GitHub:
    https://github.com/MLWhiz/data_science_blogs/tree/master/caching_stream
```