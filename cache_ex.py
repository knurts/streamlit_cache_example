"""Cache and argparse example streamlit app."""
import argparse
import getpass
import logging
import os
import streamlit as st
import sys
from time import sleep
from uuid import uuid4


_ID = 0


def check_return_against_other(key, expected_value):
    """Log analysis of return versus expected_value."""
    _url_fetch(key, _ID)


def log_step(title):
    """Log title of each step."""
    st.markdown("""**{}**""".format(title))
    logging.info("{}".format(title))


def _argparse_config():
    parser = argparse.ArgumentParser(
        description="This script can run from command line or streamlit app.")

    parser.add_argument('-b', '--boolean-example', dest='boolean_example',
                        action='store_true', default=False,
                        help='Option to be True or False.')

    parser.add_argument('-i', '--integer-example', dest='integer_example',
                        help='A number.')

    parser.add_argument('-u', '--user', dest='user',
                        help='Your username.')

    parser.add_argument('-p', '--passwd', dest='pw',
                        help='Your password.')

    parser.add_argument('-s', '--string-example', dest='string_example',
                        help='A string')

    parser.add_argument('--web', action='store_true', default=False,
                        dest='is_web',
                        help='Do not use, script will determine.')

    args = parser.parse_args()

    # App was started with no args
    if not args.string_example and not args.boolean_example and not args.integer_example:
        args.is_web = True

    print("string {} boolean {} int {} web {}".format(args.string_example, args.boolean_example, args.integer_example, args.is_web))
    if not args.is_web and args.boolean_example:
        if not args.user:
            args.user = input("Your username: ")
        if not args.pw:
            args.pw = getpass.getpass("Your password: ")

    return args


@st.cache(suppress_st_warning=False)
def _url_fetch(key, run_id_to_cache=_ID):
    sleep(6)  # pretend this makes an api call that can take a few seconds everytime


def _web_config(args=None):
    st.title("Example App")
    st.subheader("Configure options in sidebar.")
    if st.checkbox("Show Help"):
        st.markdown("Everytime the app runs, we want to make the 'expensive' call at least once."\
                    "\n\nsuppress_st_warning is False to help visualize when cache was missed."\
                    "\n\nMain processing won't run until args are completely configured.")

    st.subheader("Config:")
    st.write("Random ID: ", _ID)

    answer = st.sidebar.radio("Are you getting this?",
                            ('No', 'Yes'))
    if answer == 'Yes':
        st.write('You get it.')
        args.boolean_example = True
    else:
        st.write("I'm sorry, keep trying.")
        args.boolean_example = False

    if args.boolean_example:
        str_ex = st.sidebar.text_input("Enter your example string")
        if str_ex:
            st.write(str_ex)
            args.string_example = str_ex

        user = st.sidebar.text_input("Your Username")
        args.user = user if user else args.user
        pw = st.sidebar.text_input("Your Password", type='password')
        args.pw = pw if pw else args.pw

        int_ex = st.sidebar.text_input("Integer")
        if int_ex:
            st.write(int_ex)
            args.integer_example = int_ex
    return args


def main(args=None):
    """Run."""
    st.subheader("Output:")
    if args.boolean_example and args.integer_example and args.string_example and args.user and args.pw:
        log_step("1. Do first step. 100% Cache miss.")
        # Get most of the cache misses out of the way
        for key in range(2):
            st.write("Checking key {}".format(key))
            logging.info("Checking key {}".format(key))
            _url_fetch(key, _ID)

        log_step("2. Do another step. 1 Cache miss.")
        # Should have 1 cache miss
        for key in range(3):
            st.write("Checking key {}".format(key))
            logging.info("Checking key {}".format(key))
            check_return_against_other(key, 'A')

        log_step('3. Do final step. 100% Cache hit.')
        # Should have 100% cache hit
        for key in range(1):
            st.write("Checking key {}".format(key))
            logging.info("Checking key {}".format(key))
            _url_fetch(key, _ID)
    else:
        print("Run python3 cache_ex.py --help for usage.")


if __name__ == "__main__":
    # Generate a unique ID for each run to cache _url_fetch results
    _ID = uuid4().node
    try:
        args = _argparse_config()
        if args.is_web:
            args = _web_config(args)

        main(args)
    except IOError as e:
        st.error(e)
        sys.exit(e.errno)
