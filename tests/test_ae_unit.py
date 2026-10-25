"""
Pytest tests for the Auto Exposure system.

Covers core components: SpatialFrameAnalyzer, HistogramAnalyzer,
SceneAnalyzer, ExposureController, FlickerDetector, and AutoExposureSystem.
Uses synthetic data so no external files are needed.
"""

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.auto_exposure_system import (
    AutoExposureSystem,
    SpatialFrameAnalyzer,
    HistogramAnalyzer,
    SceneAnalyzer,
    ExposureController,
    FlickerDetector,
    SensorInfo,
    ImageStatistics,
    SceneType,
    ExposureResult,
)


def make_sensor_info():
    return SensorInfo(
        exposure_time=1 / 60,
        analog_gain=1.0,
        digital_gain=1.0,
        iso=100,
        aperture=2.0,
    )


def make_test_image(brightness=128, size=(64, 64)):
    return np.full((*size, 3), brightness, dtype=np.uint8)


class TestSpatialFrameAnalyzer:
    def test_analyze_uniform_grid(self):
        analyzer = SpatialFrameAnalyzer(grid_size=(64, 48))
        grid = np.full((64, 48), 128.0, dtype=np.float32)
        result = analyzer.analyze_spatial_distribution(grid)
        assert isinstance(result, dict)
        assert "mean_brightness" in result or len(result) > 0

    def test_analyze_gradient_grid(self):
        analyzer = SpatialFrameAnalyzer(grid_size=(64, 48))
        grid = np.zeros((64, 48), dtype=np.float32)
        for i in range(64):
            grid[i, :] = i * 4
        result = analyzer.analyze_spatial_distribution(grid)
        assert isinstance(result, dict)


class TestHistogramAnalyzer:
    def test_analyze_uniform_histogram(self):
        analyzer = HistogramAnalyzer()
        hist = np.ones(256, dtype=np.float32)
        result = analyzer.analyze_histogram(hist)
        assert isinstance(result, dict)

    def test_analyze_peaked_histogram(self):
        analyzer = HistogramAnalyzer()
        hist = np.zeros(256, dtype=np.float32)
        hist[128] = 1000.0
        result = analyzer.analyze_histogram(hist)
        assert isinstance(result, dict)


class TestSceneAnalyzer:
    def test_analyze_scene(self):
        analyzer = SceneAnalyzer()
        img = make_test_image(128)
        spatial = {"mean_brightness": 128.0, "center_brightness": 128.0}
        result = analyzer.analyze_scene(img, spatial)
        assert isinstance(result.scene_type, SceneType)
        assert 0.0 <= result.confidence <= 1.0

    def test_dark_scene(self):
        analyzer = SceneAnalyzer()
        img = make_test_image(20)
        spatial = {"mean_brightness": 20.0, "center_brightness": 20.0}
        result = analyzer.analyze_scene(img, spatial)
        assert isinstance(result.scene_type, SceneType)


class TestFlickerDetector:
    def test_no_flicker_at_standard_rate(self):
        detector = FlickerDetector()
        result = detector.detect_flicker(1 / 60)
        assert isinstance(result, bool)

    def test_adjust_exposure_time(self):
        detector = FlickerDetector()
        adjusted = detector.adjust_for_flicker(1 / 60)
        assert adjusted > 0


class TestExposureController:
    def test_calculate_tes(self):
        controller = ExposureController()
        stats = ImageStatistics(
            bayer_stats=np.full((64, 48), 128.0),
            histogram=np.ones(256),
            saturated_pixels=0,
            brightness_mean=128.0,
            brightness_std=30.0,
            center_weight=0.5,
        )
        from core.auto_exposure_system import SceneInformation
        scene = SceneInformation(
            scene_type=SceneType.OUTDOOR,
            confidence=0.8,
            face_rois=[],
            motion_level=0.0,
            dynamic_range=1.0,
        )
        tes = controller.calculate_total_exposure_sensitivity(stats, scene)
        assert tes > 0

    def test_distribute_exposure(self):
        controller = ExposureController()
        sensor = make_sensor_info()
        exposure_time, analog_gain, digital_gain = controller.distribute_exposure(
            100.0, sensor, motion_level=0.5
        )
        assert exposure_time > 0
        assert analog_gain > 0
        assert digital_gain > 0


class TestAutoExposureSystem:
    def test_init(self):
        ae = AutoExposureSystem()
        assert ae is not None

    def test_process_bright_frame(self):
        ae = AutoExposureSystem()
        img = make_test_image(200, size=(128, 128))
        sensor = make_sensor_info()
        result = ae.process_frame(img, sensor)
        assert isinstance(result, ExposureResult)
        assert result.exposure_time > 0

    def test_process_dark_frame(self):
        ae = AutoExposureSystem()
        img = make_test_image(30, size=(128, 128))
        sensor = make_sensor_info()
        result = ae.process_frame(img, sensor)
        assert isinstance(result, ExposureResult)

    def test_process_medium_frame(self):
        ae = AutoExposureSystem()
        img = make_test_image(128, size=(128, 128))
        sensor = make_sensor_info()
        result = ae.process_frame(img, sensor)
        assert isinstance(result, ExposureResult)
        assert result.total_exposure_sensitivity > 0
