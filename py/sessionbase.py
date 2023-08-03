#coding:utf-8
import re
import sys
import time
import datetime
import telnetlib
import paramiko
from io import StringIO, BytesIO
from exception import TIMEOUT,EOF

PY3 = sys.version_info[0] >= 3
if PY3:
    def _byte(i):
        return bytes([i])
else:
    def _byte(i):
        return chr(i)


class TELENETConnection(object):
    def __init__(self,timeout=30,logfile=None,maxread=2000,searchwindowsize=None):
        self.client = None
        self.before = ""
        self.after = ""
        self.timeout = timeout
        self.linesep = "\r\n"
        self.logfile = logfile
        self.maxread = maxread
        self.searchwindowsize = searchwindowsize
        self.delayafterread = 0.0001
        self.buffer_type = StringIO
        self.logfile_read = None
        self.logfile_send = None
        self.flag_eof = False
        self._buffer = self.buffer_type()

    def __str__(self):
        '''This returns a human-readable string that represents the state of
        the object. '''
        s = []
        s.append(repr(self))
        s.append('buffer (last 100 chars): %r' % self.buffer[-100:])
        s.append('before (last 100 chars): %r' % self.before[-100:] if self.before else '')
        s.append('after: %r' % (self.after,))
        s.append('match: %r' % (self.match,))
        s.append('match_index: ' + str(self.match_index))
        s.append('flag_eof: ' + str(self.flag_eof))
        s.append('timeout: ' + str(self.timeout))
        s.append('logfile: ' + str(self.logfile))
        s.append('logfile_read: ' + str(self.logfile_read))
        s.append('logfile_send: ' + str(self.logfile_send))
        s.append('maxread: ' + str(self.maxread))
        s.append('searchwindowsize: ' + str(self.searchwindowsize))
        s.append('delayafterread: ' + str(self.delayafterread))
        return '\n'.join(s)

    def _get_buffer(self):
        return self._buffer.getvalue()

    def _set_buffer(self, value):
        self._buffer = self.buffer_type()
        self._buffer.write(value)

    buffer = property(_get_buffer, _set_buffer)

    def spawn(self,hostname,port=23):
        self.client = telnetlib.Telnet(hostname,port=port)

    def _log(self, s, direction):
        if self.logfile is not None:
            self.logfile.write(s)
            self.logfile.flush()
        second_log = self.logfile_send if (direction=='send') else self.logfile_read
        if second_log is not None:
            second_log.write(s)
            second_log.flush()

    def read_nonblocking(self, size=1, timeout=None):
        """This reads data from the file descriptor.

        This is a simple implementation suitable for a regular file. Subclasses using ptys or pipes should override it.

        The timeout parameter is ignored.
        """
        try:
            s = self.client.read_very_eager()
        except EOFError as e:
            self.flag_eof = True
            print(e)
            raise EOF('End Of File (EOF). Exception style platform.')
        # if s == b'':
        #   # BSD-style EOF
        #   self.flag_eof = True
        #   raise EOF('End Of File (EOF). Empty string style platform.')
        s = str(s, encoding="utf-8")
        self._log(s, 'read')
        return s

    def sendline(self, s):
        s = s + self.linesep
        self._log(s, 'send')
        self.client.write(s.encode("ascii"))

    def _pattern_type_err(self, pattern):
        raise TypeError('got {badtype} ({badobj!r}) as pattern, must be one'\
                        ' of: {goodtypes}, connection.EOF, connection.TIMEOUT'\
                        .format(badtype=type(pattern),
                                badobj=pattern,
                                goodtypes=', '.join([repr(ast)\
                                    for ast in (str,"re.compile")])
                                )
                        )

    def compile_pattern_list(self, patterns):
        if patterns is None:
            return []
        if not isinstance(patterns, list):
            patterns = [patterns]

        # Allow dot to match \n
        compile_flags = re.DOTALL
        compiled_pattern_list = []
        for p in patterns:
            if isinstance(p, type('')):
                compiled_pattern_list.append(re.compile(p, compile_flags))
            elif p is EOF:
                compiled_pattern_list.append(EOF)
            elif p is TIMEOUT:
                compiled_pattern_list.append(TIMEOUT)
            elif isinstance(p, type(re.compile(''))):
                compiled_pattern_list.append(p)
            else:
                self._pattern_type_err(p)
        return compiled_pattern_list

    def expect(self, pattern, timeout=-1, searchwindowsize=-1):
        if timeout == -1:
            timeout = self.timeout
        compiled_pattern_list = self.compile_pattern_list(pattern)
        exp = Expecter(self, searcher_re(compiled_pattern_list), searchwindowsize)
        return exp.expect_loop(timeout)

    def close(self):
        self.client.close()


class SSHConnection(object):
    def __init__(self,timeout=30,logfile=None,maxread=2000,searchwindowsize=None):
        self.client = None
        self.channal = None
        self.before = ""
        self.after = ""
        self.timeout = timeout
        self.linesep = "\n"
        self.logfile = logfile
        self.maxread = maxread
        self.searchwindowsize = searchwindowsize
        self.delayafterread = 0.0001
        self.buffer_type = StringIO
        self.logfile_read = None
        self.logfile_send = None
        self.flag_eof = False
        self._buffer = self.buffer_type()

    def __str__(self):
        '''This returns a human-readable string that represents the state of
        the object. '''

        s = []
        s.append(repr(self))
        s.append('buffer (last 100 chars): %r' % self.buffer[-100:])
        s.append('before (last 100 chars): %r' % self.before[-100:] if self.before else '')
        s.append('after: %r' % (self.after,))
        s.append('match: %r' % (self.match,))
        s.append('match_index: ' + str(self.match_index))
        # s.append('exitstatus: ' + str(self.exitstatus))
        # if hasattr(self, 'ptyproc'):
        s.append('flag_eof: ' + str(self.flag_eof))
        # s.append('pid: ' + str(self.pid))
        # s.append('child_fd: ' + str(self.child_fd))
        # s.append('closed: ' + str(self.closed))
        s.append('timeout: ' + str(self.timeout))
        # s.append('delimiter: ' + str(self.delimiter))
        s.append('logfile: ' + str(self.logfile))
        s.append('logfile_read: ' + str(self.logfile_read))
        s.append('logfile_send: ' + str(self.logfile_send))
        s.append('maxread: ' + str(self.maxread))
        # s.append('ignorecase: ' + str(self.ignorecase))
        s.append('searchwindowsize: ' + str(self.searchwindowsize))
        # s.append('delaybeforesend: ' + str(self.delaybeforesend))
        s.append('delayafterread: ' + str(self.delayafterread))
        # s.append('delayafterterminate: ' + str(self.delayafterterminate))
        return '\n'.join(s)

    def _get_buffer(self):
        return self._buffer.getvalue()

    def _set_buffer(self, value):
        self._buffer = self.buffer_type()
        self._buffer.write(value)

    buffer = property(_get_buffer, _set_buffer)

    def spawn(self, hostname, username, password=None, pkey=None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if password:
            self.client.connect(hostname, 22, username, password=password)
        elif pkey:
            private_key = paramiko.RSAKey.from_private_key_file(pkey)
            self.client.connect(hostname, 22, username, pkey=private_key)

        self.channal = self.client.invoke_shell()
        self.channal.settimeout(5)
        self.channal.set_combine_stderr(True)


    def _log(self, s, direction):
        if self.logfile is not None:
            self.logfile.write(s)
            self.logfile.flush()
        second_log = self.logfile_send if (direction=='send') else self.logfile_read
        if second_log is not None:
            second_log.write(s)
            second_log.flush()


    def read_nonblocking(self, size=1, timeout=None):
        """This reads data from the file descriptor.

        This is a simple implementation suitable for a regular file. Subclasses using ptys or pipes should override it.

        The timeout parameter is ignored.
        """
        if (
            self.channal.closed
            or self.channal.eof_received
            or self.channal.eof_sent
            or not self.channal.active
        ):
            self.flag_eof = True
            raise EOF('End Of File (EOF). Exception style platform.')
        if self.channal.recv_ready():
            s = self.channal.recv(size)
        else:
            return None
        if s == b'':
            # BSD-style EOF
            self.flag_eof = True
            raise EOF('End Of File (EOF). Empty string style platform.')
        s = str(s, encoding="utf-8")
        self._log(s, 'read')
        return s

    def send(self, s):
        self.channal.send(s)

    def sendline(self, s):
        s = s + self.linesep
        self._log(s, 'send')
        self.channal.sendall(s)

    def sendcontrol(self, char):
        char = char.lower()
        a = ord(char)
        # please make sure char is "a-z"
        if 97 <= a <= 122:
            a = a - ord('a') + 1
            byte = _byte(a)
            self.channal.sendall(byte)

        d = {'@': 0, '`': 0,
            '[': 27, '{': 27,
            '\\': 28, '|': 28,
            ']': 29, '}': 29,
            '^': 30, '~': 30,
            '_': 31,
            '?': 127}
        if char in d:
            byte = _byte(d[char])
            self.channal.sendall(byte)


    def _pattern_type_err(self, pattern):
        raise TypeError('got {badtype} ({badobj!r}) as pattern, must be one'\
                        ' of: {goodtypes}, connection.EOF, connection.TIMEOUT'\
                        .format(badtype=type(pattern),
                                badobj=pattern,
                                goodtypes=', '.join([repr(ast)\
                                    for ast in (str,"re.compile")])
                                )
                        )

    def compile_pattern_list(self, patterns):
        if patterns is None:
            return []
        if not isinstance(patterns, list):
            patterns = [patterns]

        # Allow dot to match \n
        compile_flags = re.DOTALL
        compiled_pattern_list = []
        for p in patterns:
            if isinstance(p, type('')):
                compiled_pattern_list.append(re.compile(p, compile_flags))
            elif p is EOF:
                compiled_pattern_list.append(EOF)
            elif p is TIMEOUT:
                compiled_pattern_list.append(TIMEOUT)
            elif isinstance(p, type(re.compile(''))):
                compiled_pattern_list.append(p)
            else:
                self._pattern_type_err(p)
        return compiled_pattern_list

    def expect(self, pattern, timeout=-1, searchwindowsize=-1):
        if timeout == -1:
            timeout = self.timeout
        compiled_pattern_list = self.compile_pattern_list(pattern)
        exp = Expecter(self, searcher_re(compiled_pattern_list), searchwindowsize)
        return exp.expect_loop(timeout)

    def close(self):
        self.channal.close()
        self.client.close()

class searcher_re(object):
    '''This is regular expression string search helper for the
    spawn.expect_any() method. This helper class is for powerful
    pattern matching. For speed, see the helper class, searcher_string.

    Attributes:

        eof_index    - index of EOF, or -1
        timeout_index - index of TIMEOUT, or -1

    After a successful match by the search() method the following attributes
    are available:

        start - index into the buffer, first byte of match
        end   - index into the buffer, first byte after match
        match - the re.match object returned by a successful re.search

    '''

    def __init__(self, patterns):
        '''This creates an instance that searches for 'patterns' Where
        'patterns' may be a list or other sequence of compiled regular
        expressions, or the EOF or TIMEOUT types.'''

        self.eof_index = -1
        self.timeout_index = -1
        self._searches = []
        for n, s in zip(list(range(len(patterns))), patterns):
            if s is EOF:
                self.eof_index = n
                continue
            if s is TIMEOUT:
                self.timeout_index = n
                continue
            self._searches.append((n, s))

    def __str__(self):
        '''This returns a human-readable string that represents the state of
        the object.'''

        ss = list()
        for n, s in self._searches:
            ss.append((n, ' %d: re.compile(%r)' % (n, s.pattern)))
        ss.append((-1, 'searcher_re:'))
        if self.eof_index >= 0:
            ss.append((self.eof_index, '    %d: EOF' % self.eof_index))
        if self.timeout_index >= 0:
            ss.append((self.timeout_index, '    %d: TIMEOUT' %
                self.timeout_index))
        ss.sort()
        ss = list(zip(*ss))[1]
        return '\n'.join(ss)

    def search(self, buffer, freshlen, searchwindowsize=None):
        '''This searches 'buffer' for the first occurrence of one of the regular
        expressions. 'freshlen' must indicate the number of bytes at the end of
        'buffer' which have not been searched before.

        See class spawn for the 'searchwindowsize' argument.

        If there is a match this returns the index of that string, and sets
        'start', 'end' and 'match'. Otherwise, returns -1.'''

        first_match = None
        # 'freshlen' doesn't help here -- we cannot predict the
        # length of a match, and the re module provides no help.
        if searchwindowsize is None:
            searchstart = 0
        else:
            searchstart = max(0, len(buffer) - searchwindowsize)
        for index, s in self._searches:
            match = s.search(buffer, searchstart)
            if match is None:
                continue
            n = match.start()
            if first_match is None or n < first_match:
                first_match = n
                the_match = match
                best_index = index
        if first_match is None:
            return -1
        self.start = first_match
        self.match = the_match
        self.end = self.match.end()
        return best_index


class Expecter(object):
    def __init__(self, spawn, searcher, searchwindowsize=-1):
        self.spawn = spawn
        self.searcher = searcher
        if searchwindowsize == -1:
            searchwindowsize = spawn.searchwindowsize
        self.searchwindowsize = searchwindowsize

    def new_data(self, data):
        spawn = self.spawn
        searcher = self.searcher

        pos = spawn._buffer.tell()
        spawn._buffer.write(data)
        # spawn._before.write(data)

        # determine which chunk of data to search; if a windowsize is
        # specified, this is the *new* data + the preceding <windowsize> bytes
        if self.searchwindowsize:
            spawn._buffer.seek(max(0, pos - self.searchwindowsize))
            window = spawn._buffer.read(self.searchwindowsize + len(data))
        else:
            # otherwise, search the whole buffer (really slow for large datasets)
            window = spawn.buffer
        index = searcher.search(window, len(data))
        if index >= 0:
            # spawn.before = spawn._before.getvalue()[0:-(len(window) - searcher.start)]
            spawn.before = spawn.buffer[0:-(len(window) - searcher.start)]
            spawn._buffer.close()
            spawn._buffer = spawn.buffer_type()
            spawn._buffer.write(window[searcher.end:])
            # spawn._before = spawn.buffer_type()
            spawn.after = window[searcher.start: searcher.end]
            spawn.match = searcher.match
            spawn.match_index = index
            # Found a match
            return index
        elif self.searchwindowsize:
            spawn._buffer.close()
            spawn._buffer = spawn.buffer_type()
            spawn._buffer.write(window)

    def eof(self, err=None):
        spawn = self.spawn

        spawn.before = spawn.buffer
        spawn._buffer = spawn.buffer_type()
        # spawn._before = spawn.buffer_type()
        spawn.after = EOF
        index = self.searcher.eof_index
        if index >= 0:
            spawn.match = EOF
            spawn.match_index = index
            return index
        else:
            spawn.match = None
            spawn.match_index = None
            msg = str(spawn)
            msg += '\nsearcher: %s' % self.searcher
            if err is None:
                msg = str(err) + '\n' + msg
            raise EOF(msg)
    
    def timeout(self, err=None):
        spawn = self.spawn

        spawn.before = spawn.buffer
        spawn.after = TIMEOUT
        index = self.searcher.timeout_index
        if index >= 0:
            spawn.match = TIMEOUT
            spawn.match_index = index
            return index
        else:
            spawn.match = None
            spawn.match_index = None
            msg = str(spawn)
            msg += '\nsearcher: %s' % self.searcher
            if err is None:
                msg = str(err) + '\n' + msg
            raise TIMEOUT(msg)

    def errored(self):
        spawn = self.spawn
        spawn.before = spawn.buffer
        spawn.after = None
        spawn.match = None
        spawn.match_index = None
    
    def expect_loop(self, timeout=-1):
        """Blocking expect"""
        spawn = self.spawn

        if timeout is not None:
            end_time = time.time() + timeout

        try:
            incoming = spawn.buffer
            spawn._buffer.close()
            spawn._buffer = spawn.buffer_type()
            # spawn._before = spawn.buffer_type()
            while True:
                if incoming:
                    idx = self.new_data(incoming)
                else:
                    idx = None
                # Keep reading until exception or return.
                if idx is not None:
                    return idx
                # No match at this point
                if (timeout is not None) and (timeout < 0):
                    return self.timeout()
                    # raise TIMEOUT
                # Still have time left, so read more data
                incoming = spawn.read_nonblocking(spawn.maxread, timeout)
                if self.spawn.delayafterread is not None:
                    time.sleep(self.spawn.delayafterread)
                if timeout is not None:
                    timeout = end_time - time.time()
        except EOF as e:
            return self.eof(e)
        except TIMEOUT as e:
            return self.timeout(e)
        except:
            self.errored()
            raise


class SFTPConnection(object):
    def __init__(self,host, username, password, port=22):
        self.sftp = None
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.close()

    # @staticmethod
    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        # return self

    # @classmethod
    def put(self, localpath, remotepath):
        self.sftp.put(localpath,remotepath)

    # @classmethod
    def get(self, remotepath, localpath):
        self.sftp.get(remotepath,localpath)
    
    def mkdir(self, path, mode=511):
        self.sftp.mkdir(path, mode)

    def close(self):
        self.sftp.close()


if __name__ == '__main__':
    import os
    remote_folder = "%s/%s" %("/home/_nokadmin","cert")
    cert_folder = os.path.join("c:/commission","cert")
    cert_files = os.listdir(cert_folder)

    with SFTPConnection("10.110.62.130", "_nokadmin", "nokia123") as sftp:
        try:
            sftp.mkdir(remote_folder)
            print("create remote folder {remote_folder} success.")
        except IOError:
            print("remote_folder {remote_folder} exist")
            
        for file in cert_files:
            local_file = "%s/%s" %(cert_folder, file)
            remote_file = "%s/%s" %(remote_folder, file)
            sftp.put(local_file, remote_file)
            print(f"Put {local_file} to {remote_file} done.")
