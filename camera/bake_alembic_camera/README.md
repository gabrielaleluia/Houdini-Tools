# Bake Alembic Camera

A Python tool for SideFX Houdini that bakes an animated Alembic camera into a native Houdini camera.

## Features

- Samples the source camera's world transform over the Houdini playback range.
- Bakes translation, rotation, and scale into keyframes.
- Copies supported optical parameters when they exist on both the source and target cameras.
- Creates a native Houdini camera with the `_BAKED` suffix.
- Restores the timeline to the frame that was active before the operation.
- Wraps the operation in a single Houdini undo group.

## Requirements

- SideFX Houdini with the `hou` Python module.
- An Alembic camera object selected in the /obj context.

## Usage

1. Import the animated Alembic camera into Houdini.
2. Select the Alembic camera object.
3. Open Houdini's Python Shell.
4. Execute the contents of `bake_alembic_camera.py`.
5. The tool creates a new native camera named after the source camera with the `_BAKED` suffix.

The animation is sampled at every integer frame within the current playback range.

## Notes

- The source camera is not modified.
- The tool uses the source camera's world transform.
- Optical parameters are copied only when matching parameters are available on both nodes.
- Review the baked camera in your scene before using it in a final render, especially when the source hierarchy contains complex transforms.

## License

MIT License. See the repository's [LICENSE](../../LICENSE) file if one is added.
