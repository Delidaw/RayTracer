import time

class RenderStatistics:
    """
    Stores statistics collected during rendering.
    """

    def __init__(self):

        self.total_rays = 0

        self.captured = 0
        self.disk_hits = 0
        self.background_hits = 0

        self.start_time = None
        self.end_time = None

    def record_capture(self):

        self.total_rays += 1
        self.captured += 1


    def record_disk_hit(self):

        self.total_rays += 1
        self.disk_hits += 1


    def record_background(self):

        self.total_rays += 1
        self.background_hits += 1

    def start(self):
        """
        Starts the render timer.
        """
        self.start_time = time.time()


    def stop(self):
        """
        Stops the render timer.
        """
        self.end_time = time.time()


    def summary(
        self,
        width,
        height
    ):

        print()

        print("=" * 50)

        print("Photon Forge Render Statistics")

        print("=" * 50)

        print(f"Resolution     : {width} x {height}")
        print()

        print(f"Total Rays      : {self.total_rays}")
        print(f"Captured        : {self.captured}")
        print(f"Disk Hits       : {self.disk_hits}")
        print(f"Background Hits : {self.background_hits}")

        if self.total_rays > 0:

            print()

            print(f"Capture %       : {100*self.captured/self.total_rays:.2f}%")
            print(f"Disk %          : {100*self.disk_hits/self.total_rays:.2f}%")
            print(f"Background %    : {100*self.background_hits/self.total_rays:.2f}%")

        if (
            self.start_time is not None and
            self.end_time is not None
        ):

            elapsed = self.end_time - self.start_time

            print()

            print(f"Render Time     : {elapsed:.2f} s")

            if elapsed > 0:

                print(
                    f"Rays / Second   : {self.total_rays / elapsed:.2f}"
                )

        print("=" * 50)