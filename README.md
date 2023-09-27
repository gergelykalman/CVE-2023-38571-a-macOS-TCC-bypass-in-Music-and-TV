### Executive summary

macOS Music and TV do an insecure rename resulting in FDA by gaining full
control over the user's TCC.db

I reported this bug in separate tickets for each app, feel free to merge if
applicable.

The underlying problem is that these apps have FDA but fail to sanitize their
file operations.


### Exploit description

Music and TV are almost the same in this regard, only the paths are different.
I'm using Music as an example from here on out. For TV please check the
exploit code it is very straightforward.

Music has functionality to copy files into the user's library using
a special folder to which a user can "drop" files.

A user can simply create a file in
`~/Music/Music/Media.localized/Automatically Add to Music.localized/`

Music will take this file and do an insecure rename into
"~/Music/Music/Media.localized/Automatically Add to Music.localized/Not Added.localized".

If we use a valid TCC.db (that the exploit generates) it will get copied into
the "Not Added.localized" folder since it's not a media file. This is very
helpful, since we can redirect this rename into the real location of TCC.db
using a simple symlink race.

The exploit is technically a race condition, however it's so reliable that
I did not even implement it to retry as it always succeeds on the first try.


### Exploit details

Usage for music:
> DEBUG=1 ./librarian.py 1

Usage for tv:
> DEBUG=1 ./librarian.py 2

To reset tcc db between tests:
> launchctl stop com.apple.tccd
> launchctl start com.apple.tccd
> sleep 1
> tccutil reset All

