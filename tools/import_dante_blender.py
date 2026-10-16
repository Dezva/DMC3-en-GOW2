"""Run in Blender 4.x: import the extracted source model; no PS2 conversion yet.

blender --background --factory-startup --python-exit-code 1 --python tools/import_dante_blender.py -- \
  --addon-root /path/to/DMC3HDC-Import-Tools --resources /private/extracted --output /private/new-directory
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import bpy
from mathutils import Vector


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--addon-root", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    resources = args.resources.resolve()
    for name in ("slot_001.mod", "slot_012.mod", "texture_000.dds", "texture_001.dds", "texture_002.dds"):
        if not (resources / name).is_file():
            raise ValueError(f"Missing extracted resource: {name}")
    args.output.mkdir(parents=True, exist_ok=False)
    output = args.output.resolve()
    addon_root = args.addon_root.resolve()
    if not (addon_root / "DMC3" / "model.py").is_file():
        raise ValueError("Expected the separately obtained DMC3HDC-Import-Tools addon.")
    sys.path.insert(0, str(addon_root))
    from DMC3 import model

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    source_models = []
    source_rigs = []
    for filename, label in (("slot_001.mod", "body"), ("slot_012.mod", "coat")):
        existing_rigs = {obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"}
        model.Import(bpy.context, str(resources / filename))
        new_rigs = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE" and obj not in existing_rigs]
        if len(new_rigs) != 1:
            raise ValueError("Expected one source armature for each MOD.")
        source_rigs.append(new_rigs[0])
        source_models.append({"file": filename, "role": label,
                              "objects": model.model.objectCount, "bones": model.model.boneCount})

    # The cloth MOD has its own origin. Align it to the source body's pelvis for
    # static inspection only; this does not reproduce DMC3's runtime cloth physics.
    bpy.context.view_layer.update()
    body_rig, coat_rig = source_rigs
    pelvis = body_rig.matrix_world @ body_rig.data.bones["bone_1"].head_local
    coat_origin = coat_rig.matrix_world @ coat_rig.data.bones["bone_0"].head_local
    coat_rig.location += pelvis - coat_origin

    materials = []
    for index in range(3):
        material = bpy.data.materials.new(f"Dante_source_texture_{index}")
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        image = bpy.data.images.load(str(resources / f"texture_{index:03d}.dds"))
        image.pack()
        texture = material.node_tree.nodes.new("ShaderNodeTexImage")
        texture.image = image
        material.node_tree.links.new(texture.outputs["Color"], bsdf.inputs["Base Color"])
        material.node_tree.links.new(texture.outputs["Alpha"], bsdf.inputs["Alpha"])
        bsdf.inputs["Roughness"].default_value = 0.7
        materials.append(material)

    bpy.context.view_layer.update()
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not meshes:
        raise ValueError("The importer produced no meshes.")
    bounds = []
    mesh_stats = []
    for obj in meshes:
        match = re.search(r"_Tex:(\d+)", obj.name)
        if not match or int(match[1]) >= len(materials):
            raise ValueError(f"Unresolved source material: {obj.name}")
        obj.data.materials.clear()
        obj.data.materials.append(materials[int(match[1])])
        rig = next((modifier.object for modifier in obj.modifiers
                    if modifier.type == "ARMATURE" and modifier.object is not None), None)
        if rig is None:
            raise ValueError(f"Mesh without a source armature: {obj.name}")
        # Some upstream submeshes are parented to another mesh. glTF needs their rig parent.
        world_transform = obj.matrix_world.copy()
        obj.parent = rig
        obj.matrix_world = world_transform
        if not obj.data.uv_layers:
            raise ValueError(f"Mesh without UV coordinates: {obj.name}")
        if not all(math.isfinite(value) for vertex in obj.data.vertices for value in vertex.co):
            raise ValueError(f"Non-finite geometry: {obj.name}")
        bounds.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
        mesh_stats.append({"name": obj.name, "vertices": len(obj.data.vertices),
                           "triangles": sum(len(p.vertices) - 2 for p in obj.data.polygons),
                           "vertex_groups": len(obj.vertex_groups),
                           "unweighted_vertices": sum(not any(g.weight > 0 for g in v.groups)
                                                      for v in obj.data.vertices)})

    lower = Vector(tuple(min(point[axis] for point in bounds) for axis in range(3)))
    upper = Vector(tuple(max(point[axis] for point in bounds) for axis in range(3)))
    center = (lower + upper) * 0.5
    extent = max(upper - lower)
    if not math.isfinite(extent) or extent <= 0:
        raise ValueError("Invalid model bounds.")
    report = {"blender": bpy.app.version_string,
              "importer": "deshayu/DMC3HDC-Import-Tools",
              "tested_importer_commit": "248dec2a0b7984fbd0c74f85c7de94a09dd81e06",
              "importer_model_sha256": hashlib.sha256((addon_root / "DMC3" / "model.py").read_bytes()).hexdigest(),
              "models": source_models, "meshes": mesh_stats,
              "coat_alignment": "Static preview assumption: coat bone_0 aligned to body bone_1. Runtime cloth attachment not verified.",
              "mesh_count": len(meshes),
              "vertices": sum(m["vertices"] for m in mesh_stats),
              "triangles": sum(m["triangles"] for m in mesh_stats),
              "bounds": {"lower": list(lower), "upper": list(upper)},
              "status": "Source asset import only. Not retargeted, not PS2-ready, not tested in PCSX2."}

    bpy.ops.export_scene.gltf(filepath=str(output / "dante-source.glb"),
                              export_format="GLB", export_animations=False,
                              export_cameras=False, export_lights=False)
    camera_data = bpy.data.cameras.new("Inspection_camera")
    camera = bpy.data.objects.new("Inspection_camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = center + Vector((0, -extent * 2, extent * 0.08))
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = extent * 1.2
    bpy.context.scene.camera = camera
    for name, position, power in (("Key", (-1, -2, 2), 600), ("Fill", (1, -1, 0.5), 250)):
        light_data = bpy.data.lights.new(name, "AREA")
        light = bpy.data.objects.new(name, light_data)
        bpy.context.collection.objects.link(light)
        light.location = center + Vector(position) * extent
        light.rotation_euler = (center - light.location).to_track_quat("-Z", "Y").to_euler()
        light_data.energy = power
        light_data.shape = "DISK"
        light_data.size = extent * 2
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 16
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 768
    scene.render.resolution_y = 768
    scene.render.resolution_percentage = 100
    scene.world.color = (0.12, 0.12, 0.12)
    bpy.ops.wm.save_as_mainfile(filepath=str(output / "dante-source.blend"), check_existing=False)
    if args.render:
        scene.render.filepath = str(output / "dante-source-preview.png")
        bpy.ops.render.render(write_still=True)
    (output / "blender-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("mesh_count", "vertices", "triangles", "status")}))


if __name__ == "__main__":
    main()
