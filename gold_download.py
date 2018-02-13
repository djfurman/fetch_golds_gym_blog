from datetime import datetime  # results in faster script importing only needs
from os.path import join
from os import getcwd
import urllib2  # but sometimes you can't get around it

gym_blog_list = ['587', '1340', '747']  # gyms of interest
# This format doesn't require century hardcoding
start_date = datetime.now().strftime('%Y-%m-%d')

debug = True  # provides a debug mode param to get extra feedback


def get_storage_path(blog):
    """
    Simple method to return the storage location for incoming gym data

    :param: blog identifier
    :return: absolute path to file
    """
    save_path = join(getcwd(), 'gymdata_' + blog + '.json')
    if debug:
        print save_path
    return save_path


def main():
    """
    Makes this slightly easier to manage
    """
    for gym_blog in gym_blog_list:
        print 'Currently processing %s for date %s' % (gym_blog, start_date)
        # if using requests you can just pass query = {'targetDate': end_date}
        # This argument automatically escapes URL specials
        # and you don't have to do the string interpolation below
        apiEndpoint = ('https://www.goldsgym.com/api/gyms/%s/schedules/currentWeek?targetDate=%s') % (gym_blog, start_date)
        if debug:
            print apiEndpoint

        # Python native error handling does exactly that :)
        r = urllib2.urlopen(apiEndpoint)
        res_body = r.read()

        # Make sure our request was successful
        try:
            assert r.getcode() == 200
        except AssertionError:
            print 'Something went wrong.'
            print 'Status code: %s' % str(r.status_code)
            print r.text
            exit(-1)

        # Make sure we got a JSON file
        # This will just make sure you didn't get utf-16/32 encoding
        j = res_body.decode("utf-8")
        if debug:
            print 'Data recovered successfully.'

        # Write file
        try:
            filename = get_storage_path(gym_blog)
            file = open(filename, 'w')  # grab the file, lock it, open to write
            file.write(j)  # inject the uft-8 response
            file.close()  # always remember to close the file so it saves
            if debug:
                print '%s has been written to.' % filename
        except Exception as e:
            print 'Error: file could not be written to.'
            print type(e).__name__, e  # you can also just print e


# This allows you to still fire the main function when you just call the file
# E.g., python gold_download.py
if __name__ == '__main__':
    main()
    print 'Completed'  # always nice to tell yourself when you're done
