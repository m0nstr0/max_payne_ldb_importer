# Max Payne binary data types

This page defines the tagged values used by MP1 LDB, KF2/KFS/SKD and MP2
archives. MP1 LVL also has a separate, untagged outer stream; see
[MAXPAYNE_LVL.MD](MAXPAYNE_LVL.MD). All multi-byte values are little-endian.

## Notation

`raw` means that no type tag is stored. `T` means one tag followed by a payload.
`count` is a number of elements; `byteCount` is a number of bytes. Counts must
be nonnegative and must fit in the enclosing file or block. Do not add C/C++
structure padding between fields in the layouts on these pages.

## Tags

| Tag | Name used here | Payload bytes | Meaning |
| --- | --- | ---: | --- |
| `00` | TLong | 4 | Signed 32-bit integer |
| `01` | TULong | 4 | Unsigned 32-bit integer |
| `02`, `12`, `13`, `14` | TInt | 4, 3, 2, 1 | Signed integer |
| `03`, `0f`, `10`, `11` | TUInt | 4, 3, 2, 1 | Unsigned integer |
| `04` | TShort | 2 | Signed 16-bit integer |
| `05` | TUShort | 2 | Unsigned 16-bit integer |
| `06` | TChar | 1 | Character byte; preserve its bits |
| `07` | TSChar | 1 | Signed 8-bit integer |
| `08` | TUChar | 1 | Unsigned 8-bit integer |
| `09` | TFloat | 4 | IEEE 754 binary32 |
| `0a` | TDouble | 8 | IEEE 754 binary64 |
| `0d` | TString | Variable | Tagged signed byte count, then string bytes |
| `0e` | TBool | 1 | Boolean; write 0 or 1 |
| `15` | TVector2f | 8 | Two raw binary32 values |
| `16` | TVector3f | 12 | Three raw binary32 values |
| `17` | TVector4f | 16 | Four raw binary32 values |
| `18` | TMatrix2x2f | 16 | Four raw binary32 values |
| `19` | TMatrix3x3f | 36 | Nine raw binary32 values |
| `1a` | TMatrix4x3f | 48 | Twelve raw binary32 values |
| `1b` | TMatrix4x4f | 64 | Sixteen raw binary32 values |
| `26` | TFloat16 | 2 | Separate 16-bit float payload |

`TULong`, `TUShort` and `TUChar` are distinct types. Do not replace their tags
with compact TUInt tags merely because their numerical values are equal.
The 16-bit float is not another encoding of the four-byte TFloat field.

## Integers

Sign-extend TInt and TShort payloads. Zero-extend unsigned payloads.
For example, `14 ff` is TInt(-1), while `11 ff` is TUInt(255).
A signed 24-bit payload `00 00 80` represents -8388608.
A missing payload is an error, not the integer zero.

Historical names beginning with `M_` refer to the same tagged types. The C
spelling `long` in older pages always means four bytes here, regardless of the
host platform's `sizeof(long)`.

## Strings

```text
raw u8 tag = 0d
TInt byteCount
raw u8 bytes[byteCount]
```

The count excludes any terminator. No trailing NUL is required or added.
The source encoding is not universally established. Preserve original bytes;
ASCII names are common, but decoding every string as UTF-8 can reject valid
assets. The Python SDK uses a reversible Latin-1 byte view. This is a storage
choice, not a claim about the author's code page.

MP2 LDB also stores NUL-terminated strings in a shared raw pool. References to
that pool are offsets, not TString values; see [MP2 LDB](MAXPAYNE2_LDB.MD).
MP1 LVL CString lengths use different rules.

## Vectors and matrices

Each vector or matrix has one tag, followed by its raw float components.
Do not put a float tag before each component. A 4x3 matrix stores four rows
of three values. Transform conventions belong to the containing format;
changing row/column conventions is an import operation, not a byte-layout rule.

## Collection markers

| Marker | Container | Header after the marker |
| --- | --- | --- |
| `1c` | Vector | TInt elementCount |
| `1d` | Set | TInt elementCount |
| `1f` | Map | TInt entryCount |

Each element follows its own schema. A map entry can contain several fields,
so its count is not the number of following tags. Preserve entry order and
unknown values when round-tripping a source file. A collection marker is not
a general permission to parse its body without knowing the element type.

## Chunks

KF2-family and MP2 LV2 chunks use a raw header:

```text
raw u8  tag = 0c
raw u32 id
raw u32 version
raw u32 totalSize
raw u8  payload[totalSize - 13]
```

`totalSize` includes the 13-byte header. A child must fit entirely inside its
parent. Skip unknown chunks by size. Never search their payloads for a byte
that looks like another tag. MP1/MP2 LDB sections are not automatically chunks.
