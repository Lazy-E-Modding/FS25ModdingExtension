# i3D Color Node Addon for Blender

## Overview

The **I3DColorNodeAddon** is a powerful tool designed to automate and simplify various modding tasks in **Blender**. This script provides functionality for manipulating materials, creating nodes, and extracting custom properties. Specifically, it can create an **RGB node** in the Shader Editor from a custom property (`customParameter_colorScale`) in a material, streamlining workflows for modders.

## Features

- Retrieves the `customParameter_colorScale` property from the active material.
- Parses the RGBA values from the custom property.
- Automatically creates an **RGB node** in the Shader Editor with the parsed color values.
- Easy-to-use interface, integrated into the Shader Editor's **Add Menu**.

## Installation

1. **Download the Script**:  
   Download the `I3DColorNodeAddon` file and save it to your computer.

2. **Install the Add-On**:
   - Open Blender.
   - Go to **Edit** > **Preferences** > **Add-ons**.
   - Click the **Install...** button and select the downloaded `i3DColorNodeAddon.zip` file.
   - Enable the add-on by checking the box next to its name in the Add-ons list.

3. **Using the Script**:
   - Open the **Shader Editor** in Blender.
   - Right-click in the editor and select **Add > Custom RGB Node** from the context menu.
   - The script will automatically read the `customParameter_colorScale` from the active material (if it exists) and create an RGB node with the corresponding RGBA values.

## License

The Lazy E Modding Script is **open-source software** licensed under the **GNU General Public License, version 3** (GPL-3.0).

By using, modifying, or redistributing this script, you agree to the terms and conditions outlined in the [License Agreement](LICENSE.md).

## GNU General Public License (GPL-3.0)

### Terms:
- You may **use**, **modify**, and **distribute** copies of this script in both its original and modified forms under the same terms as this license.
- If you redistribute the script (either modified or unmodified), you must include the full source code and retain this license.
- You may not add any additional restrictions on the rights granted by the GPL. For example, you may not add a license that restricts the ability of others to modify or redistribute the software.
- You are allowed to **use** the software for commercial purposes, but you must ensure that any redistribution complies with the GPL-3.0.

The full license text can be found in the [LICENSE.md](LICENSE.md) file.

### DISCLAIMER:
This script is provided **as-is**, without any warranty or guarantee of any kind, either express or implied, including but not limited to the warranties of merchantability or fitness for a particular purpose.

## Limitations

- The script only works if the selected object has a valid material with the custom property `customParameter_colorScale`.
- The custom property must be in the format `r g b alpha` (e.g., `0.4508 0.0176 0.0232 1.0`).
- Ensure that your material has a valid node tree enabled for the script to function properly.

## Troubleshooting

- **No RGB Node Created**: Ensure that the active material contains the `customParameter_colorScale` custom property in the correct format.
- **Script Not Working**: Double-check that the add-on is enabled in Blender’s preferences.

## Contributing

Contributions to this script are not currently accepted. For feature requests or bug reports, please contact **Lazy E Modding** directly.

## Contact

For any questions or support, please contact **Lazy E Modding** at [contact@lazyemodding.com].

---

## Disclaimer

The Lazy E Modding Script is provided "as-is," without any warranty of any kind. The script creator is not responsible for any loss of data, hardware failure, or other damages arising from the use of this tool.

---

## Acknowledgments

- This script was created by **Lazy E Modding**.
- Blender Python API documentation and resources were invaluable in developing this tool.
