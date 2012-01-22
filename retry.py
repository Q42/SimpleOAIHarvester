import time, math

def retry(f, tries=3, delay=3, backoff=2):
  """Retries a function or method until it returns True.

  delay sets the initial delay, and backoff sets how much the delay should
  lengthen after each failure. backoff must be greater than 1, or else it
  isn't really a backoff. tries must be at least 0, and delay greater than
  0."""

  if backoff <= 1:
    raise ValueError("backoff must be greater than 1")

  tries = math.floor(tries)
  if tries < 0:
    raise ValueError("tries must be 0 or greater")

  if delay <= 0:
    raise ValueError("delay must be greater than 0")

  def f_retry(*args, **kwargs):
    mtries, mdelay = tries, delay # make mutable

    while True:
      if mtries == 0:
        raise Exception("out of retries")

      try:
        rv = f(*args, **kwargs) # first attempt
      except:
        print "retrying"
        mtries -= 1      # consume an attempt
        time.sleep(mdelay) # wait...
        mdelay *= backoff  # make future wait longer
      else:
        return rv

  return f_retry
