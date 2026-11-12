import hou

def bake_alembic_camera():

    # ================================================
    # CONFIGURATION
    # ================================================

    selected = hou.selectedNodes()

    if not selected:
        hou.ui.displayMessage(
            "Selecione o objeto da camera Alembic."
        )
        return

    source = selected[0]

    if not hasattr(source, "worldTransform"):
        hou.ui.displayMessage(
            "O nó selecionado nao possui worldTransform().\\n"
            "Selecione o objeto da camera Alembic."
        )
        return

    start_frame, end_frame = hou.playbar.frameRange()

    start_frame = int(start_frame)
    end_frame = int(end_frame)

    original_frame = hou.frame()

    obj = hou.node("/obj")

    # ================================================
    # CREATE CAMERA
    # ================================================

    camera_name = source.name() + "_BAKED"

    camera = obj.createNode("cam", camera_name)

    # Set XYZ rotation order when available
    rotation_order = camera.parm("rOrd")

    if rotation_order:
        if "xyz" in rotation_order.menuItems():
            rotation_order.set("xyz")

    # ================================================
    # PARAMETERS TO BAKE
    # ================================================

    transform_data = {
        "t": [[], [], []],
        "r": [[], [], []],
        "s": [[], [], []]
    }

    optical_parameters = [
        "focal",
        "aperture",
        "near",
        "far",
        "resx",
        "resy",
        "aspect",
        "orthowidth"
    ]

    optical_data = {}

    for name in optical_parameters:

        source_parm = source.parm(name)
        target_parm = camera.parm(name)

        if source_parm and target_parm:
            optical_data[name] = []

    # ================================================
    # SAMPLE ALEMBIC CAMERA
    # ================================================

    try:

        for frame in range(start_frame, end_frame + 1):

            hou.setFrame(frame)

            # Get world transform
            matrix = source.worldTransform()

            # Decompose matrix
            components = matrix.explode(
                transform_order="srt",
                rotate_order="xyz"
            )

            translate = components["translate"]
            rotate = components["rotate"]
            scale = components["scale"]

            # Store transform values
            for i in range(3):

                transform_data["t"][i].append(
                    (frame, translate[i])
                )

                transform_data["r"][i].append(
                    (frame, rotate[i])
                )

                transform_data["s"][i].append(
                    (frame, scale[i])
                )

            # Store optical parameters
            for name in optical_data:

                value = source.parm(name).eval()

                optical_data[name].append(
                    (frame, value)
                )

        # ============================================
        # APPLY TRANSFORM KEYFRAMES
        # ============================================

        for channel, components in transform_data.items():

            parm_tuple = camera.parmTuple(channel)

            for axis in range(3):

                keys = []

                for frame, value in components[axis]:

                    key = hou.Keyframe()

                    key.setFrame(frame)
                    key.setValue(value)

                    keys.append(key)

                parm_tuple[axis].setKeyframes(keys)

        # ============================================
        # APPLY OPTICAL KEYFRAMES
        # ============================================

        for name, values in optical_data.items():

            parm = camera.parm(name)

            keys = []

            for frame, value in values:

                key = hou.Keyframe()

                key.setFrame(frame)
                key.setValue(value)

                keys.append(key)

            parm.setKeyframes(keys)

        # ============================================
        # FINISH
        # ================================================

        hou.setFrame(start_frame)

        camera.setSelected(True, clear_all_selected=True)

        camera.moveToGoodPosition()

        hou.ui.displayMessage(
            "ALEMBIC CAMERA BAKE COMPLETE!\\n\\n"
            "Source: " + source.path() + "\\n"
            "Camera: " + camera.path() + "\\n"
            "Start Frame: " + str(start_frame) + "\\n"
            "End Frame: " + str(end_frame) + "\\n"
            "Total Frames: " + str(end_frame - start_frame + 1)
        )

    except Exception as error:

        camera.destroy()

        hou.ui.displayMessage(
            "ERROR DURING CAMERA BAKE:\\n\\n" + str(error)
        )

    finally:

        hou.setFrame(original_frame)


# ================================================
# EXECUTE
# ================================================

with hou.undos.group("Bake Alembic Camera"):
    bake_alembic_camera()
