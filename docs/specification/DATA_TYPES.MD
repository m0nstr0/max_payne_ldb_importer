# Table of contents

* [Max Payne data types](#max-payne-data-types)
  * [Overview](#overview)
  * [List of the types ](#list-of-the-types)
  * [Types description](#types-description)
    * [M_Long](#m_long)
    * [M_Unsigned_Long](#m_unsigned_long)
    * [M_Short](#m_short)
    * [M_Unsigned_Short](#m_unsigned_short)
    * [M_Char](#m_char)
    * [M_Signed_Char](#m_signed_char)
    * [M_Unsigned_Char](#m_unsigned_char)
    * [M_Float](#m_float)
    * [M_Double](#m_double)
    * [M_Bool](#m_bool)
    * [M_Int](#m_int)
    * [M_Vector2](#m_vector2)
    * [M_Vector3](#m_vector3)
    * [M_Vector4](#m_vector4)
    * [M_String](#m_string)
    * [M_Matrix2x2](#m_matrix2x2)
    * [M_Matrix3x3](#m_matrix3x3)
    * [M_Matrix4x3](#m_matrix4x3)
    * [M_Matrix4x4](#m_matrix4x4)

## Max Payne data types

### Overview 

Max Payne stores data in the following format:

```{Tag}{Data}```

* **Tag** - The Tag of the type from the table below.
* **Data** - The data.

## List of the types

 | Tag  | Data Size | Alias              |
 |------|-----------|--------------------|
 | 0x00 | 4 bytes   | M_Long             |
 | 0x01 | 4 bytes   | M_Unsigned_Long    |
 | 0x04 | 2 bytes   | M_Short            |
 | 0x05 | 2 bytes   | M_Unsigned_Short   |
 | 0x06 | 1 bytes   | M_Char             |
 | 0x07 | 1 bytes   | M_Signed_Char      |
 | 0x08 | 1 bytes   | M_Unsigned_Char    |
 | 0x09 | 4 bytes   | M_Float            |
 | 0x0A | 8 bytes   | M_Double           |
 | 0x0E | 1 bytes   | M_Bool             |
 | 0x02 | 4 bytes   | M_Int              |
 | 0x12 | 3 bytes   | M_Int              |
 | 0x13 | 2 bytes   | M_Int              |
 | 0x14 | 1 bytes   | M_Int              |
 | 0x03 | 4 bytes   | M_Unsigned_Int     |
 | 0x0F | 3 bytes   | M_Unsigned_Int     |
 | 0x10 | 2 bytes   | M_Unsigned_Int     |
 | 0x11 | 1 bytes   | M_Unsigned_Int     |
 | 0x15 | 8 bytes   | M_Vector2          |
 | 0x16 | 12 bytes  | M_Vector3          |
 | 0x17 | 16 bytes  | M_Vector4          |
 | 0x26 | 2 bytes   | M_Float            |
 | 0x0D | ---       | M_String           |
 | 0x18 | 16 bytes  | M_Matrix2x2        |
 | 0x19 | 19 bytes  | M_Matrix3x3        |
 | 0x1A | 48 bytes  | M_Matrix4x3        |
 | 0x1B | 64 bytes  | M_Matrix4x4        |

## Types description

### M_Long

Format:

```{0x00}{long}```

* **0x00** - The Tag of the type.
* **long** - 4 bytes long type.

### M_Unsigned_Long

Format:

```{0x01}{unsigned long}```

* **0x01** - The Tag of the type.
* **unsigned long** - 4 bytes unsigned long type.

### M_Short

Format:

```{0x04}{short}```

* **0x04** - The Tag of the type.
* **short** - 2 bytes short type.

### M_Unsigned_Short

Format:

```{0x05}{unsigned short}```

* **0x05** - The Tag of the type.
* **unsigned short** - 2 bytes unsigned short type.

### M_Char

Format:

```{0x06}{char}```

* **0x06** - The Tag of the type.
* **char** - 1 byte char type.

### M_Signed_Char

Format:

```{0x07}{signed char}```

* **0x07** - The Tag of the type.
* **signed char** - 1 byte signed char type.

### M_Unsigned_Char

Format:

```{0x08}{unsigned char}```

* **0x08** - The Tag of the type.
* **unsigned char** - 1 byte unsigned char type.

### M_Float

Formats:

```{0x09}{float}```

* **0x09** - The Tag of the type.
* **float** - 4 bytes float type.

```{0x26}{byte[2]}```

* **0x26** - The Tag of the type.
* **byte[2]** - Array of the 2 bytes. (It's should be converted to 4 bytes float).

### M_Double

Format:

```{0x0A}{double}```

* **0x0A** - The Tag of the type.
* **double** - 8 bytes double type.

### M_Bool

Format:

```{0x0E}{bool}```

* **0x0E** - The Tag of the type.
* **bool** - 1 byte bool type.

### M_Int

Formats:

```{0x02}{int}```

* **0x02** - The Tag of the type.
* **int** - 4 bytes int type.

```{0x12}{byte[3]}```

* **0x12** - The Tag of the type.
* **byte[3]** - Array of the 3 bytes. (It's should be converted to 4 bytes int)
 
```{0x13}{byte[2]}```

* **0x13** - The Tag of the type.
* **byte[2]** - Array of the 2 bytes. (It's should be converted to 4 bytes int)

```{0x14}{byte}```

* **0x14** - The Tag of the type.
* **byte** - 1 byte. (It's should be converted to 4 bytes int)

### M_Unsigned_Int

Formats:

```{0x03}{unsigned int}```

* **0x03** - The Tag of the type.
* **unsigned int** - 4 bytes unsigned int type.

```{0x0F}{byte[3]}```

* **0x0F** - The Tag of the type.
* **byte[3]** - Array of the 3 bytes. (It's should be converted to 4 bytes unsigned int)
 
```{0x10}{byte[2]}```

* **0x10** - The Tag of the type.
* **byte[2]** - Array of the 2 bytes. (It's should be converted to 4 bytes unsigned int)

```{0x11}{byte}```

* **0x11** - The Tag of the type.
* **byte** - 1 byte. (It's should be converted to 4 bytes unsigned int)

### M_Vector2

Format:

```{0x15}{float[2]}```

* **0x15** - The Tag of the type.
* **float[2]** - Array of the 4 bytes floats.

### M_Vector3

Format:

```{0x16}{float[3]}```

* **0x16** - The Tag of the type.
* **float[3]** - Array of the 4 bytes floats.
 
### M_Vector4

Format:

```{0x17}{float[4]}```

* **0x17** - The Tag of the type.
* **float[4]** - Array of the 4 bytes floats.

### M_String

Format:

```{0x0D}{M_Int}{Characters[M_Int]}```

* **0x0D** - The Tag of the type.
* **M_Int** - Max Payne's integer type. The Length of the Characters array.
* **Characters[M_Int]** - Array of the 1 byte characters.

### M_Matrix2x2

Format:

```{0x18}{float[4]}```

* **0x18** - The Tag of the type.
* **float[4]** - Array of the 4 bytes floats.

### M_Matrix3x3

Format:

```{0x19}{float[9]}```

* **0x19** - The Tag of the type.
* **float[9]** - Array of the 4 bytes floats.

### M_Matrix4x3

Format:

```{0x1A}{float[12]}```

* **0x1A** - The Tag of the type.
* **float[12]** - Array of the 4 bytes floats.

### M_Matrix4x4

Format:

```{0x1B}{float[16]}```

* **0x1B** - The Tag of the type.
* **float[16]** - Array of the 4 bytes floats.
