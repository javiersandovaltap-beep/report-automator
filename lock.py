import os


class LockAcquisitionError(Exception):
    """Raised when the lock file already exists."""


def acquire_lock(lock_path: str) -> int:
    """
    Atomically create the lock file via os.open with O_CREAT | O_EXCL | O_WRONLY,
    write the current process ID into it, close and return the file descriptor.
    On FileExistsError, raise LockAcquisitionError with a message including lock_path.
    """
    try:
        # Open the file with O_CREAT | O_EXCL | O_WRONLY to atomically create it
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            # Write the current process ID to the lock file
            pid_str = str(os.getpid())
            os.write(fd, pid_str.encode())
        finally:
            # Always close the file descriptor
            os.close(fd)
        return fd
    except FileExistsError:
        raise LockAcquisitionError(f"Lock file already exists: {lock_path}")


def release_lock(lock_path: str) -> None:
    """
    Remove the lock file if it exists.
    Must never raise if the file is already gone.
    """
    try:
        os.unlink(lock_path)
    except FileNotFoundError:
        # File already gone - this is acceptable
        pass