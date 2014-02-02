import re, time

from cookielib import CookieJar, LoadError,Cookie


class StrCookieJar(CookieJar):
    """CookieJar that can be loaded from and saved to a file."""

    def __init__(self, cookieStr=None, delayload=True, policy=None):
        """
        Cookies are NOT loaded from the named file until either the .load() or
        .revert() method is called.

        """
        CookieJar.__init__(self, policy)
        if cookieStr is not None:
            if 1:
                cookieStr+""
                self.load(cookieStr)
            else:
                raise ValueError("cookieStr must be string-like")

    def dump(self, ignore_discard=True, ignore_expires=True):
        rtn_val=""
        for cookie in self:
            if not ignore_discard and cookie.discard:
                continue
            if not ignore_expires and cookie.is_expired(now):
                continue
            if cookie.secure: secure = "TRUE"
            else: secure = "FALSE"
            if cookie.domain.startswith("."): initial_dot = "TRUE"
            else: initial_dot = "FALSE"
            if cookie.expires is not None:
                expires = str(cookie.expires)
            else:
                expires = ""
            if cookie.value is None:
                # cookies.txt regards 'Set-Cookie: foo' as a cookie
                # with no name, whereas cookielib regards it as a
                # cookie with no value.
                name = ""
                value = cookie.name
            else:
                name = cookie.name
            value = cookie.value
            rtn_val+="\t".join([cookie.domain, initial_dot, cookie.path,
                               secure, expires, name, value])+"\n"
        return rtn_val
        
    def load(self, loadStr, ignore_discard=True , ignore_expires=True):
        now = time.time()

        lines=loadStr.split('\n')
        for line in lines:
            if line == "": break

            # last field may be absent, so keep any trailing tab
            if line.endswith("\n"): line = line[:-1]

            # skip comments and blank lines XXX what is $ for?
            if (line.strip().startswith(("#", "$")) or
                line.strip() == ""):
                continue

            domain, domain_specified, path, secure, expires, name, value = \
                    line.split("\t")
            secure = (secure == "TRUE")
            domain_specified = (domain_specified == "TRUE")
            if name == "":
                # cookies.txt regards 'Set-Cookie: foo' as a cookie
                # with no name, whereas cookielib regards it as a
                # cookie with no value.
                name = value
                value = None

            initial_dot = domain.startswith(".")
            assert domain_specified == initial_dot

            discard = False
            if expires == "":
                expires = None
                discard = True

            # assume path_specified is false
            c = Cookie(0, name, value,
                           None, False,
                           domain, domain_specified, initial_dot,
                           path, False,
                           secure,
                           expires,
                           discard,
                           None,
                           None,
                           {})
            if not ignore_discard and c.discard:
                continue
            if not ignore_expires and c.is_expired(now):
                continue
            self.set_cookie(c)

