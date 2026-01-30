import numpy as np
import math

# ------------------------------
# Утилиты
# ------------------------------

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-8 else v

def build_triplanar_basis(normal):
    """
    Построение локального базиса (T, B, N)
    """
    N = normalize(normal)
    up = np.array([0.0, 1.0, 0.0])
    if abs(np.dot(N, up)) > 0.99:
        up = np.array([1.0, 0.0, 0.0])
    T = normalize(np.cross(up, N))
    B = np.cross(N, T)
    return np.column_stack((T, B, N))  # 3x3 матрица

def triplanar_weights(normal, sharpness=4.0):
    n = np.abs(normal) ** sharpness
    return n / np.sum(n)

def checker_texture(uv):
    x, y = int(math.floor(uv[0])), int(math.floor(uv[1]))
    return np.array([1.0, 1.0, 1.0]) if (x + y) % 2 == 0 else np.array([0.0, 0.0, 0.0])

# ------------------------------
# Преобразование TBN с scale и rotation
# ------------------------------

def transform_tbn(TBN, scale=(1.0,1.0), rotation=0.0):
    """
    Встраиваем scale и rotation в локальные оси T и B
    """
    sx, sy = scale
    c = math.cos(rotation)
    s = math.sin(rotation)

    T = TBN[:,0]
    B = TBN[:,1]
    N = TBN[:,2]

    # Поворот + scale в плоскости T-B
    T_new = T * sx * c - B * sy * s
    B_new = T * sx * s + B * sy * c

    return np.column_stack((T_new, B_new, N))

# ------------------------------
# Triplanar mapping
# ------------------------------

def triplanar_mapping(position, normal, scale=(1.0,1.0), rotation=0.0, sharpness=4.0):
    pos = np.array(position)
    nrm = normalize(np.array(normal))

    # Вес каждой проекции
    w = triplanar_weights(nrm, sharpness)

    # Базисы для каждой проекции (упрощённо ось проекции = нормаль плоскости)
    basis_x = build_triplanar_basis([0,0.406737,-0.913546])
    basis_y = build_triplanar_basis([-1,0,0])
    basis_z = build_triplanar_basis([0.0, 0.913546, 0.406737])

    # Встраиваем трансформацию в TBN
    basis_x = transform_tbn(basis_x, scale, rotation)
    basis_y = transform_tbn(basis_y, scale, rotation)
    basis_z = transform_tbn(basis_z, scale, rotation)

    # UV для каждой плоскости
    uv_x = np.array([pos[1], pos[2], 1.0])  # YZ
    uv_y = np.array([pos[0], pos[2], 1.0])  # XZ
    uv_z = np.array([pos[0], pos[1], 1.0])  # XY

    # Применяем TBN для UV (только T и B)
    uv_x_tb = np.array([basis_x[:,0] @ uv_x, basis_x[:,1] @ uv_x])
    uv_y_tb = np.array([basis_y[:,0] @ uv_y, basis_y[:,1] @ uv_y])
    uv_z_tb = np.array([basis_z[:,0] @ uv_z, basis_z[:,1] @ uv_z])

    print(f"uv_x_tb {uv_x_tb}")
    print(f"uv_y_tb {uv_y_tb}")
    print(f"uv_z_tb {uv_z_tb}")

    # Сэмплинг текстуры
    col_x = checker_texture(uv_x_tb)
    col_y = checker_texture(uv_y_tb)
    col_z = checker_texture(uv_z_tb)

    # Блендинг по весам
    final_color = col_x * w[0] + col_y * w[1] + col_z * w[2]

    return final_color

# ------------------------------
# Пример использования
# ------------------------------

if __name__ == "__main__":
    pos = [2.0, -0.779789171645927, 1.25936146321677]
    normal = [0.0, 0.913546, 0.406737]
    color = triplanar_mapping(
        pos,
        normal,
        scale=(1, 1),
        rotation=math.radians(0),
        sharpness=0.0
    )
    print("Triplanar color:", color)