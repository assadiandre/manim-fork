"""Profile a complex 3D manim scene to identify bottlenecks."""
import cProfile
import pstats
from manim import *

class ProfileScene(ThreeDScene):
    def construct(self):
        # Complex 3D scene: axes + surface + rotating camera
        axes = ThreeDAxes()
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
        )
        surface.set_style(fill_opacity=0.7, stroke_width=0.5)

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, surface)

        # 5 second animation with camera rotation + transform
        self.begin_ambient_camera_rotation(rate=0.3)
        self.play(
            surface.animate.shift(UP),
            run_time=5,
        )
        self.stop_ambient_camera_rotation()

if __name__ == "__main__":
    import time

    # Time the full render
    start = time.perf_counter()

    profiler = cProfile.Profile()
    profiler.enable()

    with tempconfig({
        "quality": "low_quality",
        "preview": False,
        "disable_caching": True,
    }):
        scene = ProfileScene()
        scene.render()

    profiler.disable()
    elapsed = time.perf_counter() - start

    print(f"\n{'='*60}")
    print(f"TOTAL WALL TIME: {elapsed:.2f}s")
    print(f"{'='*60}\n")

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    print("TOP 40 BY CUMULATIVE TIME:")
    stats.print_stats(40)

    print("\nTOP 30 BY TOTAL (SELF) TIME:")
    stats.sort_stats("tottime")
    stats.print_stats(30)
