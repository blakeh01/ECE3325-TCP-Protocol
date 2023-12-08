# ECE3325-TCP-Protocol
Custom data protocol sent via. a TCP connection.

The custom protocol uses a basic structure:
(HEADER) (DATA) (CHECKSUM)

Where header has information about the length of the following transmission, and checksum which is the sum of the entire
message.
