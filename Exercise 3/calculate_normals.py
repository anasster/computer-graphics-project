import numpy as np


def calculate_normals(verts, faces):
    # Function that calculates the normals belonging to each vertex of the object

    # Initialize an empty array for the normal vectors
    normals = np.zeros_like(verts)
    vertex_count = np.zeros(verts.shape[1])
    # Iterate each triangle
    for face in faces.T:
        # Save each triangle's index
        v1_idx, v2_idx, v3_idx = face
        # Calculate the number of triangles this vertex is in
        vertex_count[v1_idx] += 1
        vertex_count[v2_idx] += 1
        vertex_count[v3_idx] += 1
        # Calculate the triangle's edge vectors
        v1 = verts[:, v1_idx] - verts[:, v2_idx] 
        v2 = verts[:, v1_idx] - verts[:, v3_idx] 
        # Calculate the triangle's normal
        face_normal = np.cross(v1, v2) 
        # A vertex's normal is estimated by the average of the face normals this vertex belong to
        normals[:, v1_idx] = normals[:, v1_idx] + face_normal 
        normals[:, v2_idx] = normals[:, v2_idx] + face_normal 
        normals[:, v3_idx] = normals[:, v3_idx] + face_normal 
    
    # Divide each vertex's normal by the number of triangles it is a part of, to take the average
    normals = np.divide(normals, vertex_count)
    
    return normals / np.linalg.norm(normals, axis=0)