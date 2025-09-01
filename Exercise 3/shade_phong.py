import numpy as np
from light import *
from interpolate_vectors import *
import cmath


def shade_phong(verts_p, verts_n, verts_c, bcoords, cam_pos, mat, lights, light_amb, X):
    # Function that shades a triangle according to the Gouraud model, where the vertices' color is calculated by the Phong illumination model
    colors = np.zeros((3, 3))
    normals = verts_n
    for i in range(3):
        colors[:, i] = light(bcoords, verts_n[:, i], verts_c[:, i], cam_pos, mat, lights, light_amb)
    verts = np.int64(verts_p)

    # Create two arrays with the sorted indices of x and y coordinates of the vertices
    sorted_x = np.argsort(verts[0, :])
    sorted_y = np.argsort(verts[1, :])


    # In this part, we check for all possible triangle forms, as well as check whether the vertices form a straight line
    # Case 1: The triangle has no horizontal sides (default)
    tri_case = 1

    # Now, we check for the rest two cases where two of the triangle's points are on the same horizontal line, as well as the special case that 
    # the vertices form a line. Note that in all cases, the vertices need to be sorted in a counter-clockwise manner, starting from the bottom vertex


    # Case 2: The first two points (increasing y order) are on the same horizontal line
    if verts[1, sorted_y[0]] == verts[1, sorted_y[1]]:
        tri_case = 2 
        if verts[0, sorted_y[1]] < verts[0, sorted_y[0]]:
            sorted_y = np.array([sorted_y[1], sorted_y[0], sorted_y[2]])
    
    # Case 3: The last two points (increasing y order) are on the same horizontal side
    if verts[1, sorted_y[1]] == verts[1, sorted_y[2]]:
        tri_case = 3
    
    # Case 0: All points belong to the same straight line
    if verts[1, sorted_y[0]] == verts[1, sorted_y[1]] and verts[1, sorted_y[1]] == verts[1, sorted_y[2]]:
        tri_case = 0
        # Sort vertices and colors by increasing x order
        verts = verts[:, sorted_x]
        colors = colors[:, sorted_x]
        for x in range(verts[0, 0], verts[0, 1]):
            y_line = verts[1, 0] # y coordinate of the straight line
            # Paint the line
            color = interpolate_vectors(verts[:, 0], verts[:, 1], colors[:, 0], colors[:, 1], x, 1)
            X[y_line, x, :] = color
        for x in range(verts[0, 1], verts[0, 2] + 1):
            y_line = verts[1, 1] # y coordinate of the straight line
            # Paint the line
            color = interpolate_vectors(verts[:, 1], verts[:, 2], colors[:, 1], colors[:, 2], x, 1)
            X[y_line, x, :] = color
        return X

    # We want to sort the vertices in a counterclockwise manner, starting from the "lowest" lefftmost point (according to its y coordinate)
    if verts[1, sorted_y[0]] != verts[1, sorted_y[2]]:
        # Due to the clockwise sorting method, we want to check whether the high point or the middle point will have the index 1
        # Create two complex vectors to find the angle between point 0, point 1 and point 2 respectively
        w1 = (verts[0, sorted_y[2]] - verts[0, sorted_y[0]]) + 1j * (verts[1, sorted_y[2]] - verts[1, sorted_y[0]])
        w2 = (verts[0, sorted_y[1]] - verts[0, sorted_y[0]]) + 1j * (verts[1, sorted_y[1]] - verts[1, sorted_y[0]])
        if cmath.phase(w1) < cmath.phase(w2):
            sorted_y = np.array([sorted_y[0], sorted_y[2], sorted_y[1]])

    # Since all cases have been checked, we sort the vertices, the colors and the normals
    verts = verts[:, sorted_y]
    colors = colors[:, sorted_y]
    normals = normals[:, sorted_y]

    # In this part, we will calculate the effective points and sides of the triangle, according to its shape.
    effective_points = np.zeros((2, 2)) # Each time the scanline goes further, the effective points of the triangle will be updated
    effective_sides = np.zeros(2) # Each triangle has two sides that are active during the scanning
    slope_inv = np.zeros(3) # The inverse slope of each triangle's side

    # Initialize the above arrays according to the triangle's shape
    if tri_case == 1:
        # No horizontal sides
        effective_points[:, 0] = verts[:, 0]
        effective_points[:, 1] = verts[:, 0]
        # The first effective point is the first vertex of the triangle

        # The inverse slope of the i-th side is the inverse slope between points i, i + 1 
        slope_inv[0] = (verts[0, 1] - verts[0, 0]) / (verts[1, 1] - verts[1, 0])
        slope_inv[1] = (verts[0, 2] - verts[0, 1]) / (verts[1, 2] - verts[1, 1])
        slope_inv[2] = (verts[0, 0] - verts[0, 2]) / (verts[1, 0] - verts[1, 2])

        # The first two effective sides according to the sorting are 0-1 and 0-2
        effective_sides[0] = slope_inv[2]
        effective_sides[1] = slope_inv[0]
    
    elif tri_case == 2:
        # First two points form horizontal side
        effective_points[:, 0] = verts[:, 0]
        effective_points[:, 1] = verts[:, 1]
        # The scanning begins with the first two effective points being the first two vertices

        # The horizontal line's inverse slope will be infinite
        slope_inv[0] = np.Inf
        slope_inv[1] = (verts[0, 2] - verts[0, 1]) / (verts[1, 2] - verts[1, 1])
        slope_inv[2] = (verts[0, 0] - verts[0, 2]) / (verts[1, 0] - verts[1, 2])

        # The effective sides will be the non-horizontal sides
        effective_sides[0] = slope_inv[2]
        effective_sides[1] = slope_inv[1]
    
    elif tri_case == 3:
        # Last two points form a horizontal line
        effective_points[:, 0] = verts[:, 0]
        effective_points[:, 1] = verts[:, 0]
        # The scanning again begins at the "single" vertex

        # The horizontal side's inverse slope will be infinite
        slope_inv[0] = (verts[0, 1] - verts[0, 0]) / (verts[1, 1] - verts[1, 0])
        slope_inv[1] = np.Inf
        slope_inv[2] = (verts[0, 0] - verts[0, 2]) / (verts[1, 0] - verts[1, 2])

        # The effective sides will be the non-horizontal sides again
        effective_sides[0] = slope_inv[2]
        effective_sides[1] = slope_inv[0]
    
    # Now that the effective points and sides of the triangle have been initialized, we shade the triangle according to the 3 cases
    if tri_case ==1:
        # Here we have two conditions; The first is when the highest point is to the right of the middle point, and the other one is the
        # opposite condition
        # First case: High point right of middle point
        if verts[1, 1] > verts[1, 2]:
            for y in range(verts[1, 0], verts[1, 2]):
                # Update the effective points' coordinates
                effective_points[:, 0] = np.array([effective_points[0, 0] + effective_sides[0], effective_points[1, 0] + 1])
                effective_points[:, 1] = np.array([effective_points[0, 1] + effective_sides[1], effective_points[1, 1] + 1])
                p1 = np.int64(np.round(effective_points[:, 0]))
                p2 = np.int64(np.round(effective_points[:, 1]))
                # Find the rounded effective points' colors using interpolation across the y axis, and color the triangle's side points
                color_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], colors[:, 0], colors[:, 2], y + 1, 2)
                color_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], colors[:, 0], colors[:, 1], y + 1, 2)
                norm_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], normals[:, 0], normals[:, 2], y + 1, 2)
                norm_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], normals[:, 0], normals[:, 1], y + 1, 2)
                X[p1[1], p1[0], :] = light(bcoords, norm_y1, color_y1, cam_pos, mat, lights, light_amb)
                X[p2[1], p2[0], :] = light(bcoords, norm_y2, color_y2, cam_pos, mat, lights, light_amb)
                # Color the horizontal line between p1, p2
                for x in range(p1[0] + 1, p2[0]):
                    color_x = interpolate_vectors(p1, p2, color_y1, color_y2, x, 1)
                    norm_x = interpolate_vectors(p1, p2, norm_y1, norm_y2, x, 1)
                    X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)
            # Update the effective edges
            effective_sides[0] = slope_inv[1]
            effective_sides[1] = slope_inv[0]
            for y in range(verts[1, 2], verts[1, 1]):
                # Update the effective points' coordinates
                effective_points[:, 0] = np.array([effective_points[0, 0] + effective_sides[0], effective_points[1, 0] + 1])
                effective_points[:, 1] = np.array([effective_points[0, 1] + effective_sides[1], effective_points[1, 1] + 1])
                p1 = np.int64(np.round(effective_points[:, 0]))
                p2 = np.int64(np.round(effective_points[:, 1]))
                # Find the rounded effective points' colors using interpolation across the y axis, and color the triangle's side points
                color_y1 = interpolate_vectors(verts[:, 2], verts[:, 1], colors[:, 2], colors[:, 1], y + 1, 2)
                color_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], colors[:, 0], colors[:, 1], y + 1, 2)
                norm_y1 = interpolate_vectors(verts[:, 2], verts[:, 1], normals[:, 2], normals[:, 1], y + 1, 2)
                norm_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], normals[:, 0], normals[:, 1], y + 1, 2)
                X[p1[1], p1[0], :] = light(bcoords, norm_y1, color_y1, cam_pos, mat, lights, light_amb)
                X[p2[1], p2[0], :] = light(bcoords, norm_y2, color_y2, cam_pos, mat, lights, light_amb)
                # Color the horizontal line between p1, p2
                for x in range(p1[0] + 1, p2[0]):
                    color_x = interpolate_vectors(p1, p2, color_y1, color_y2, x, 1)
                    norm_x = interpolate_vectors(p1, p2, norm_y1, norm_y2, x, 1)
                    X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)

        # Second case: Middle point right of high point
        elif verts[1, 2] > verts[1, 1]:
            for y in range(verts[1, 0], verts[1, 1]):
                # Update the effective points' coordinates
                effective_points[:, 0] = np.array([effective_points[0, 0] + effective_sides[0], effective_points[1, 0] + 1])
                effective_points[:, 1] = np.array([effective_points[0, 1] + effective_sides[1], effective_points[1, 1] + 1])
                p1 = np.int64(np.round(effective_points[:, 0]))
                p2 = np.int64(np.round(effective_points[:, 1]))
                # Find the rounded effective points' colors using interpolation across the y axis, and color the triangle's side points
                color_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], colors[:, 0], colors[:, 2], y + 1, 2)
                color_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], colors[:, 0], colors[:, 1], y + 1, 2)
                norm_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], normals[:, 0], normals[:, 2], y + 1, 2)
                norm_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], normals[:, 0], normals[:, 1], y + 1, 2)
                X[p1[1], p1[0], :] = light(bcoords, norm_y1, color_y1, cam_pos, mat, lights, light_amb)
                X[p2[1], p2[0], :] = light(bcoords, norm_y2, color_y2, cam_pos, mat, lights, light_amb)
                # Color the horizontal line between p1, p2
                for x in range(p1[0] + 1, p2[0]):
                    color_x = interpolate_vectors(p1, p2, color_y1, color_y2, x, 1)
                    norm_x = interpolate_vectors(p1, p2, norm_y1, norm_y2, x, 1)
                    X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)
            # Update the effective sides
            effective_sides[0] = slope_inv[2]
            effective_sides[1] = slope_inv[1]
            for y in range(verts[1, 1], verts[1, 2]):
                # Update the effective points' coordinates
                effective_points[:, 0] = np.array([effective_points[0, 0] + effective_sides[0], effective_points[1, 0] + 1])
                effective_points[:, 1] = np.array([effective_points[0, 1] + effective_sides[1], effective_points[1, 1] + 1])
                p1 = np.int64(np.round(effective_points[:, 0]))
                p2 = np.int64(np.round(effective_points[:, 1]))
                # Find the rounded effective points' colors using interpolation across the y axis, and color the triangle's side points
                color_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], colors[:, 0], colors[:, 2], y + 1, 2)
                color_y2 = interpolate_vectors(verts[:, 1], verts[:, 2], colors[:, 1], colors[:, 2], y + 1, 2)
                norm_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], normals[:, 0], normals[:, 2], y + 1, 2)
                norm_y2 = interpolate_vectors(verts[:, 1], verts[:, 2], normals[:, 1], normals[:, 2], y + 1, 2)
                X[p1[1], p1[0], :] = light(bcoords, norm_y1, color_y1, cam_pos, mat, lights, light_amb)
                X[p2[1], p2[0], :] = light(bcoords, norm_y2, color_y2, cam_pos, mat, lights, light_amb)
                # Color the horizontal line between p1, p2
                for x in range(p1[0] + 1, p2[0]):
                    color_x = interpolate_vectors(p1, p2, color_y1, color_y2, x, 1)
                    norm_x = interpolate_vectors(p1, p2, norm_y1, norm_y2, x, 1)
                    X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)
        
    elif tri_case == 2:
        # Here there are no special sub-cases. We begin with the effective points being the two lower vertices
        p1 = np.int64(np.round(np.array([effective_points[0, 0], effective_points[1, 0]])))
        p2 = np.int64(np.round(np.array([effective_points[0, 1], effective_points[1, 1]])))
        # Paint the bottom side
        for x in range(p1[0] + 1, p2[0]):
            color_x = interpolate_vectors(p1, p2, colors[:, 0], colors[:, 1], x, 1)
            norm_x = interpolate_vectors(p1, p2, normals[:, 0], normals[:, 1], x, 1)
            X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)
        for y in range(verts[1, 0], verts[1, 2]):
            # Update the effective points' coordinates
            effective_points[:, 0] = np.array([effective_points[0, 0] + effective_sides[0], effective_points[1, 0] + 1])
            effective_points[:, 1] = np.array([effective_points[0, 1] + effective_sides[1], effective_points[1, 1] + 1])
            p1 = np.int64(np.round(effective_points[:, 0]))
            p2 = np.int64(np.round(effective_points[:, 1]))
            # Find the rounded effective points' colors and normals using interpolation across the y axis, and color the triangle's side points
            color_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], colors[:, 0], colors[:, 2], y + 1, 2)
            color_y2 = interpolate_vectors(verts[:, 1], verts[:, 2], colors[:, 1], colors[:, 2], y + 1, 2)
            norm_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], normals[:, 0], normals[:, 2], y + 1, 2)
            norm_y2 = interpolate_vectors(verts[:, 1], verts[:, 2], normals[:, 1], normals[:, 2], y + 1, 2)
            X[p1[1], p1[0], :] = light(bcoords, norm_y1, color_y1, cam_pos, mat, lights, light_amb)
            X[p2[1], p2[0], :] = light(bcoords, norm_y2, color_y2, cam_pos, mat, lights, light_amb)
            # Color the horizontal line between p1, p2
            for x in range(p1[0] + 1, p2[0]):
                color_x = interpolate_vectors(p1, p2, color_y1, color_y2, x, 1)
                norm_x = interpolate_vectors(p1, p2, norm_y1, norm_y2, x, 1)
                X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)
    
    elif tri_case == 3:
        for y in range(verts[1, 0], verts[1, 2]):    
            # Here, there is only one initial effective point, therefore we begin by updating immediately
            effective_points[:, 0] = np.array([effective_points[0, 0] + effective_sides[0], effective_points[1, 0] + 1])
            effective_points[:, 1] = np.array([effective_points[0, 1] + effective_sides[1], effective_points[1, 1] + 1])
            p1 = np.int64(np.round(effective_points[:, 0]))
            p2 = np.int64(np.round(effective_points[:, 1]))
            # Find the rounded effective points' colors using interpolation across the y axis, and color the triangle's side points
            color_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], colors[:, 0], colors[:, 2], y + 1, 2)
            color_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], colors[:, 0], colors[:, 1], y + 1, 2)
            norm_y1 = interpolate_vectors(verts[:, 0], verts[:, 2], normals[:, 0], normals[:, 2], y + 1, 2)
            norm_y2 = interpolate_vectors(verts[:, 0], verts[:, 1], normals[:, 0], normals[:, 1], y + 1, 2)
            X[p1[1], p1[0], :] = light(bcoords, norm_y1, color_y1, cam_pos, mat, lights, light_amb)
            X[p2[1], p2[0], :] = light(bcoords, norm_y2, color_y2, cam_pos, mat, lights, light_amb)
            # Color the horizontal line between p1, p2
            for x in range(p1[0] + 1, p2[0]):
                color_x = interpolate_vectors(p1, p2, color_y1, color_y2, x, 1)
                norm_x = interpolate_vectors(p1, p2, norm_y1, norm_y2, x, 1)
                X[p1[1], x, :] = light(bcoords, norm_x, color_x, cam_pos, mat, lights, light_amb)

    for i in range(3):
        X[verts[1, i], verts[0, i], :] = colors[:, i]
    
    return X