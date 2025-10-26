import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import warnings
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import pickle

warnings.filterwarnings('ignore')

class NeuralNetworkFeatureExtractor:
    """Extract ML-ready features for neural network models"""
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def extract_ml_features(self, features, sr, hop_length):
        """Extract features suitable for ML models"""
        n_frames = features['zcr'].shape[1]
        ml_features = []
        
        for i in range(n_frames):
            frame_features = {
                'zcr': features['zcr'][0, i],
                'mfcc_mean': np.mean(features['mfcc'][:, i]),
                'mfcc_std': np.std(features['mfcc'][:, i]),
                'spec_centroid': features['spec_centroid'][0, i],
                'spec_rolloff': features['spec_rolloff'][0, i],
                'spec_bandwidth': features['spec_bandwidth'][0, i],
                'rms': features['rms'][0, i],
                'harmonic_energy': features['harmonic_strength'][0, i],
                'percussive_energy': features['percussive_strength'][0, i],
                'zero_mean': np.mean(features['y_percussive'][i*512:(i+1)*512]),
                'chroma_mean': np.mean(features['chroma'][:, i]),
            }
            ml_features.append(frame_features)
        
        return ml_features

class RealTimeProcessor:
    """Process audio in real-time chunks"""
    
    def __init__(self, chunk_size=2048, sr=22050):
        self.chunk_size = chunk_size
        self.sr = sr
        self.buffer = np.array([])
        self.detections = []
    
    def process_chunk(self, chunk, detector):
        """Process audio chunks in real-time"""
        self.buffer = np.append(self.buffer, chunk)
        
        if len(self.buffer) >= self.chunk_size:
            features = detector.extract_comprehensive_features(self.buffer)
            claps = detector.detect_clap(self.buffer, features)
            whistles = detector.detect_whistle(self.buffer, features)
            
            self.detections.extend(claps)
            self.detections.extend(whistles)
            
            # Keep only recent data
            self.buffer = self.buffer[-self.chunk_size:]
        
        return self.detections

class AudioSegmentation:
    """Segment audio into different regions"""
    
    @staticmethod
    def segment_by_energy(y, sr, hop_length=512, threshold=0.02):
        """Segment audio by energy levels"""
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        
        # Find high and low energy regions
        high_energy = rms > np.mean(rms) + np.std(rms)
        
        segments = []
        in_segment = False
        start_frame = 0
        
        for i, is_high in enumerate(high_energy):
            if is_high and not in_segment:
                start_frame = i
                in_segment = True
            elif not is_high and in_segment:
                segments.append({
                    'start': librosa.frames_to_time(start_frame, sr=sr, hop_length=hop_length),
                    'end': librosa.frames_to_time(i, sr=sr, hop_length=hop_length),
                    'energy': np.mean(rms[start_frame:i])
                })
                in_segment = False
        
        return segments

class AdvancedPatternMatcher:
    """Match complex audio patterns"""
    
    @staticmethod
    def match_harmonic_series(fft_data, fundamental_freq, sr, tolerance=0.1):
        """Detect harmonic series patterns (for whistles)"""
        freqs = np.fft.fftfreq(len(fft_data), 1/sr)
        magnitudes = np.abs(fft_data)
        
        harmonic_peaks = []
        for harmonic in range(1, 8):
            expected_freq = fundamental_freq * harmonic
            freq_idx = np.argmin(np.abs(freqs - expected_freq))
            
            if magnitudes[freq_idx] > np.max(magnitudes) * 0.1:
                harmonic_peaks.append({
                    'harmonic': harmonic,
                    'frequency': freqs[freq_idx],
                    'magnitude': magnitudes[freq_idx]
                })
        
        return harmonic_peaks
    
    @staticmethod
    def detect_frequency_drift(features, sr, hop_length):
        """Detect frequency changes over time (whistle quality)"""
        spec_centroid = features['spec_centroid'][0]
        
        # Calculate frequency drift rate
        drift = np.diff(spec_centroid)
        drift_rate = np.abs(drift)
        
        return {
            'mean_drift': np.mean(drift_rate),
            'max_drift': np.max(drift_rate),
            'stability': 1 - (np.std(drift_rate) / (np.max(spec_centroid) + 1e-8))
        }

class NoiseAnalyzer:
    """Analyze and handle noise"""
    
    @staticmethod
    def estimate_noise_profile(y, sr, duration=0.5):
        """Estimate noise from audio beginning"""
        sample_count = int(sr * duration)
        noise_samples = y[:sample_count]
        
        return {
            'noise_mean': np.mean(np.abs(noise_samples)),
            'noise_std': np.std(np.abs(noise_samples)),
            'noise_power': np.mean(noise_samples**2)
        }
    
    @staticmethod
    def snr_estimate(y, sr):
        """Estimate Signal-to-Noise Ratio"""
        noise_profile = NoiseAnalyzer.estimate_noise_profile(y, sr)
        signal_power = np.mean(y**2)
        noise_power = noise_profile['noise_power']
        
        snr_db = 10 * np.log10(signal_power / (noise_power + 1e-8))
        return snr_db

class EventClassifier:
    """Advanced event classification"""
    
    @staticmethod
    def classify_sound(features, frame_idx, sr, hop_length):
        """Classify sound event type with detailed characteristics"""
        
        zcr = features['zcr'][0, frame_idx]
        spec_centroid = features['spec_centroid'][0, frame_idx]
        spec_rolloff = features['spec_rolloff'][0, frame_idx]
        harmonic = features['harmonic_strength'][0, frame_idx]
        percussive = features['percussive_strength'][0, frame_idx]
        
        # Calculate ratios
        harmonic_percussive_ratio = harmonic / (percussive + 1e-8)
        spectral_ratio = spec_centroid / (spec_rolloff + 1e-8)
        
        classification = {
            'is_clap': percussive > harmonic and zcr > np.median(features['zcr']),
            'is_whistle': harmonic > percussive and zcr < np.median(features['zcr']),
            'is_noise': abs(harmonic - percussive) < 0.1,
            'harmonic_percussive_ratio': harmonic_percussive_ratio,
            'spectral_ratio': spectral_ratio,
            'confidence_clap': percussive * (1 - zcr),
            'confidence_whistle': harmonic * zcr,
        }
        
        return classification

class TemporalAnalyzer:
    """Analyze temporal patterns and rhythms"""
    
    @staticmethod
    def extract_timing_patterns(detections, sr, hop_length):
        """Extract timing patterns between events"""
        if len(detections) < 2:
            return None
        
        times = librosa.frames_to_time(np.array([d[0] for d in detections]), 
                                      sr=sr, hop_length=hop_length)
        intervals = np.diff(times)
        
        return {
            'intervals': intervals,
            'mean_interval': np.mean(intervals),
            'std_interval': np.std(intervals),
            'is_regular': np.std(intervals) / (np.mean(intervals) + 1e-8) < 0.3,
            'bpm': 60 / (np.mean(intervals) + 1e-8) if len(intervals) > 0 else 0
        }

class ModelTrainer:
    """Simple model trainer for custom datasets"""
    
    def __init__(self):
        self.training_data = {'clap': [], 'whistle': [], 'noise': []}
        self.model_params = None
    
    def add_training_sample(self, features, label):
        """Add training sample"""
        if label in self.training_data:
            self.training_data[label].append(features)
    
    def train_simple_model(self):
        """Train a simple statistical model"""
        self.model_params = {}
        
        for label, samples in self.training_data.items():
            if samples:
                samples_array = np.array(samples)
                self.model_params[label] = {
                    'mean': np.mean(samples_array, axis=0),
                    'std': np.std(samples_array, axis=0)
                }
        
        return self.model_params
    
    def save_model(self, filename):
        """Save trained model"""
        with open(filename, 'wb') as f:
            pickle.dump(self.model_params, f)
    
    def load_model(self, filename):
        """Load trained model"""
        with open(filename, 'rb') as f:
            self.model_params = pickle.load(f)

class UltraAdvancedSoundEventDetector:
    """
    Ultra-Advanced Sound Event Detection System
    With ML integration, real-time processing, and advanced analysis
    """
    
    def __init__(self, sr=22050, frame_length=2048, hop_length=512):
        self.sr = sr
        self.frame_length = frame_length
        self.hop_length = hop_length
        self.clap_threshold = 0.55
        self.whistle_threshold = 0.50
        
        # Initialize sub-modules
        self.ml_extractor = NeuralNetworkFeatureExtractor()
        self.realtime_processor = RealTimeProcessor(sr=sr)
        self.segmentation = AudioSegmentation()
        self.pattern_matcher = AdvancedPatternMatcher()
        self.noise_analyzer = NoiseAnalyzer()
        self.event_classifier = EventClassifier()
        self.temporal_analyzer = TemporalAnalyzer()
        self.model_trainer = ModelTrainer()
        
        self.detection_history = []
    
    def load_audio(self, file_path):
        """Load audio file"""
        try:
            if not Path(file_path).exists():
                print(f"❌ File not found: {file_path}")
                return None, None
            
            y, sr = librosa.load(file_path, sr=self.sr)
            print(f"✅ Audio loaded: {len(y)/sr:.2f}s @ {sr}Hz")
            return y, sr
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None
    
    def extract_comprehensive_features(self, y):
        """Extract all advanced features"""
        print("\n📊 Extracting comprehensive features...")
        
        S = librosa.feature.melspectrogram(y=y, sr=self.sr, n_fft=self.frame_length,
                                          hop_length=self.hop_length, n_mels=128)
        S_db = librosa.power_to_db(S, ref=np.max)
        
        mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=13)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
        
        zcr = librosa.feature.zero_crossing_rate(y, frame_length=self.frame_length,
                                                 hop_length=self.hop_length)
        
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=self.sr)
        spec_rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sr)
        spec_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=self.sr)
        
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=self.sr)
        onset_env = librosa.onset.onset_strength(y=y, sr=self.sr)
        
        rms = librosa.feature.rms(y=y, frame_length=self.frame_length,
                                  hop_length=self.hop_length)
        
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        harmonic_strength = librosa.feature.rms(y=y_harmonic, frame_length=self.frame_length,
                                               hop_length=self.hop_length)
        percussive_strength = librosa.feature.rms(y=y_percussive, frame_length=self.frame_length,
                                                 hop_length=self.hop_length)
        
        spec_flux = np.sqrt(np.sum(np.diff(S_db, axis=1)**2, axis=0))
        
        # NEW: Spectral contrast (texture features)
        spec_contrast = librosa.feature.spectral_contrast(y=y, sr=self.sr)
        
        # NEW: Tempogram (rhythm)
        tempogram = librosa.feature.tempogram(onset_env=onset_env, sr=self.sr)
        
        # NEW: Chroma energy normalized
        chroma_energy = np.sqrt(np.sum(chroma_stft**2, axis=0))
        
        # NEW: Spectral variation
        spec_variation = np.std(S_db, axis=0)
        
        # NEW: Peak-to-average ratio
        mag_spec = np.abs(librosa.stft(y, n_fft=self.frame_length, 
                                       hop_length=self.hop_length))
        peak_avg_ratio = np.max(mag_spec, axis=0) / (np.mean(mag_spec, axis=0) + 1e-8)
        
        # NEW: Subband energies
        subband_energy = self._extract_subband_energy(y)
        
        print("✅ Feature extraction complete")
        
        return {
            'melspec': S_db,
            'mfcc': mfcc,
            'mfcc_delta': mfcc_delta,
            'mfcc_delta2': mfcc_delta2,
            'zcr': zcr,
            'spec_centroid': spec_centroid,
            'spec_rolloff': spec_rolloff,
            'spec_bandwidth': spec_bandwidth,
            'chroma': chroma_stft,
            'chroma_energy': chroma_energy,
            'onset_env': onset_env,
            'rms': rms,
            'harmonic_strength': harmonic_strength,
            'percussive_strength': percussive_strength,
            'spectral_flux': spec_flux,
            'spec_contrast': spec_contrast,
            'tempogram': tempogram,
            'spectral_variation': spec_variation,
            'peak_avg_ratio': peak_avg_ratio,
            'subband_energy': subband_energy,
            'y_harmonic': y_harmonic,
            'y_percussive': y_percussive
        }
    
    def _extract_subband_energy(self, y):
        """Extract energy in different frequency subbands"""
        stft = np.abs(librosa.stft(y, n_fft=self.frame_length, 
                                   hop_length=self.hop_length))
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=self.frame_length)
        
        subbands = {
            'bass': (0, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'high': (4000, 8000),
            'ultra_high': (8000, self.sr//2)
        }
        
        subband_energy = {}
        for name, (low, high) in subbands.items():
            mask = (freqs >= low) & (freqs < high)
            subband_energy[name] = np.sum(stft[mask, :], axis=0)
        
        return subband_energy
    
    def detect_clap_advanced(self, y, features):
        """Advanced clap detection with neural-inspired scoring"""
        print("\n🔍 Advanced clap detection...")
        
        zcr = features['zcr'][0]
        onset_env = features['onset_env']
        percussive = features['percussive_strength'][0]
        peak_avg = features['peak_avg_ratio']
        subband = features['subband_energy']
        
        # Normalize features
        zcr_norm = (zcr - np.mean(zcr)) / (np.std(zcr) + 1e-8)
        percussive_norm = (percussive - np.mean(percussive)) / (np.std(percussive) + 1e-8)
        peak_norm = (peak_avg - np.mean(peak_avg)) / (np.std(peak_avg) + 1e-8)
        
        # NEW: Subband-based scoring (clap has energy across all bands)
        bass_energy = subband['bass']
        high_energy = subband['high']
        subband_ratio = high_energy / (bass_energy + 1e-8)
        subband_norm = (subband_ratio - np.mean(subband_ratio)) / (np.std(subband_ratio) + 1e-8)
        
        # Find peaks
        peaks, properties = signal.find_peaks(onset_env, 
                                             height=np.max(onset_env)*0.2,
                                             distance=int(self.sr/self.hop_length*0.1))
        
        clap_candidates = []
        
        for peak in peaks:
            # Neural-inspired weighted scoring
            clap_score = (
                0.25 * (1 if zcr_norm[peak] > 0.4 else 0) +
                0.25 * (1 if percussive_norm[peak] > 0.3 else 0) +
                0.20 * (1 if peak_norm[peak] > 0.5 else 0) +
                0.20 * (1 if subband_norm[peak] > 0.3 else 0) +
                0.10 * (properties['peak_heights'][list(peaks).index(peak)] / np.max(onset_env))
            )
            
            if clap_score > self.clap_threshold:
                clap_candidates.append((peak, clap_score))
        
        clap_frames = self._filter_close_detections(clap_candidates, 
                                                    min_distance=int(0.3*self.sr/self.hop_length))
        
        print(f"✅ Found {len(clap_frames)} clap(s)")
        return clap_frames
    
    def detect_whistle_advanced(self, y, features):
        """Advanced whistle detection with harmonic analysis"""
        print("\n🔍 Advanced whistle detection...")
        
        zcr = features['zcr'][0]
        mfcc = features['mfcc']
        harmonic = features['harmonic_strength'][0]
        chroma_energy = features['chroma_energy']
        spec_variation = features['spectral_variation']
        
        # Normalize
        zcr_norm = (zcr - np.mean(zcr)) / (np.std(zcr) + 1e-8)
        harmonic_norm = (harmonic - np.mean(harmonic)) / (np.std(harmonic) + 1e-8)
        chroma_norm = (chroma_energy - np.mean(chroma_energy)) / (np.std(chroma_energy) + 1e-8)
        
        # NEW: Spectral stability (whistles are stable)
        spec_var_norm = (spec_variation - np.mean(spec_variation)) / (np.std(spec_variation) + 1e-8)
        
        mfcc_variance = np.var(mfcc, axis=0)
        mfcc_var_norm = (mfcc_variance - np.mean(mfcc_variance)) / (np.std(mfcc_variance) + 1e-8)
        
        whistle_candidates = []
        
        for i in range(len(zcr)):
            # Whistles have: low ZCR, high harmonic, stable spectrum, high chroma
            whistle_score = (
                0.25 * (1 if zcr_norm[i] < -0.3 else 0) +
                0.25 * (1 if harmonic_norm[i] > 0.3 else 0) +
                0.20 * (1 if mfcc_var_norm[i] < 0.3 else 0) +
                0.15 * (1 if chroma_norm[i] > 0.2 else 0) +
                0.15 * (1 if spec_var_norm[i] < 0.5 else 0)
            )
            
            if whistle_score > self.whistle_threshold:
                whistle_candidates.append((i, whistle_score))
        
        whistle_frames = self._cluster_frames(whistle_candidates, 
                                             min_duration=int(0.1*self.sr/self.hop_length))
        
        print(f"✅ Found {len(whistle_frames)} whistle(s)")
        return whistle_frames
    
    def _filter_close_detections(self, candidates, min_distance):
        """Filter duplicate detections"""
        if not candidates:
            return []
        
        candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        filtered = []
        
        for frame, score in candidates:
            if not any(abs(frame - f[0]) < min_distance for f in filtered):
                filtered.append((frame, score))
        
        return sorted(filtered, key=lambda x: x[0])
    
    def _cluster_frames(self, candidates, min_duration):
        """Cluster consecutive frames"""
        if not candidates:
            return []
        
        candidates = sorted(candidates, key=lambda x: x[0])
        clusters = []
        current_cluster = [candidates[0]]
        
        for i in range(1, len(candidates)):
            if candidates[i][0] - current_cluster[-1][0] < min_duration:
                current_cluster.append(candidates[i])
            else:
                best_frame = max(current_cluster, key=lambda x: x[1])
                clusters.append(best_frame)
                current_cluster = [candidates[i]]
        
        if current_cluster:
            best_frame = max(current_cluster, key=lambda x: x[1])
            clusters.append(best_frame)
        
        return sorted(clusters, key=lambda x: x[0])
    
    def analyze_detection_quality(self, y, features, detections):
        """Analyze quality of detections"""
        print("\n📈 Analyzing detection quality...")
        
        snr = self.noise_analyzer.snr_estimate(y, self.sr)
        segments = self.segmentation.segment_by_energy(y, self.sr, self.hop_length)
        timing = self.temporal_analyzer.extract_timing_patterns(detections, self.sr, self.hop_length)
        
        quality_metrics = {
            'snr_db': snr,
            'num_segments': len(segments),
            'num_detections': len(detections),
            'timing_info': timing,
            'audio_quality': 'HIGH' if snr > 20 else 'MEDIUM' if snr > 10 else 'LOW'
        }
        
        return quality_metrics
    
    def detect(self, file_path, plot=True, save_results=False, enable_realtime=False):
        """Complete detection pipeline"""
        print("\n" + "="*70)
        print("🎵 ULTRA-ADVANCED SOUND EVENT DETECTION SYSTEM v2.0")
        print("="*70)
        
        y, sr = self.load_audio(file_path)
        if y is None:
            return None
        
        # NEW: Noise analysis
        noise_profile = self.noise_analyzer.estimate_noise_profile(y, sr)
        print(f"\n🔊 Noise Profile - Mean: {noise_profile['noise_mean']:.4f}, "
              f"Std: {noise_profile['noise_std']:.4f}")
        
        features = self.extract_comprehensive_features(y)
        
        # Advanced detections
        clap_frames = self.detect_clap_advanced(y, features)
        whistle_frames = self.detect_whistle_advanced(y, features)
        
        all_detections = clap_frames + whistle_frames
        
        # NEW: Quality analysis
        quality_metrics = self.analyze_detection_quality(y, features, all_detections)
        
        clap_times = librosa.frames_to_time(np.array([f[0] for f in clap_frames]),
                                           sr=self.sr, hop_length=self.hop_length)
        whistle_times = librosa.frames_to_time(np.array([f[0] for f in whistle_frames]),
                                              sr=self.sr, hop_length=self.hop_length)
        
        # NEW: ML feature extraction
        ml_features = self.ml_extractor.extract_ml_features(features, self.sr, self.hop_length)
        
        results = {
            'clap': clap_frames,
            'whistle': whistle_frames,
            'clap_times': clap_times,
            'whistle_times': whistle_times,
            'features': features,
            'audio': y,
            'file': file_path,
            'timestamp': datetime.now().isoformat(),
            'quality_metrics': quality_metrics,
            'noise_profile': noise_profile,
            'ml_features': ml_features
        }
        
        self.detection_history.append(results)
        
        if plot:
            self.plot_advanced_results(y, features, clap_frames, whistle_frames, quality_metrics)
        
        if save_results:
            self.save_results_advanced(results)
        
        self.print_advanced_summary(results)
        
        return results
    
    def plot_advanced_results(self, y, features, clap_frames, whistle_frames, quality_metrics):
        """Advanced visualization with quality metrics"""
        print("\n📊 Generating advanced visualizations...")
        
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(8, 3, hspace=0.4, wspace=0.3)
        
        frames_axis = np.arange(len(features['zcr'][0]))
        time_axis = librosa.frames_to_time(frames_axis, sr=self.sr, hop_length=self.hop_length)
        
        # 1. Waveform
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(np.arange(len(y))/self.sr, y, alpha=0.7, linewidth=0.8, color='steelblue')
        ax1.set_title('Audio Waveform with Noise Profile', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True, alpha=0.3)
        
        # 2. Mel Spectrogram
        ax2 = fig.add_subplot(gs[1:3, :])
        img = librosa.display.specshow(features['melspec'], sr=self.sr, 
                                       hop_length=self.hop_length, x_axis='time',
                                       y_axis='mel', ax=ax2)
        ax2.set_title('Mel Spectrogram with Detections', fontsize=13, fontweight='bold')
        plt.colorbar(img, ax=ax2, label='dB')
        
        # 3. ZCR
        ax3 = fig.add_subplot(gs[3, 0])
        ax3.plot(time_axis, features['zcr'][0], label='ZCR', alpha=0.7)
        if len(clap_frames) > 0:
            clap_times = librosa.frames_to_time(np.array([f[0] for f in clap_frames]),
                                               sr=self.sr, hop_length=self.hop_length)
            ax3.scatter(clap_times, features['zcr'][0][[f[0] for f in clap_frames]], 
                       color='red', s=100, marker='o', label='Clap', zorder=5)
        ax3.set_title('Zero Crossing Rate', fontsize=11, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Spectral Features
        ax4 = fig.add_subplot(gs[3, 1])
        ax4.plot(time_axis, features['spec_centroid'][0], label='Centroid', alpha=0.7)
        ax4.plot(time_axis, features['spec_rolloff'][0], label='Rolloff', alpha=0.7)
        ax4.set_title('Spectral Features', fontsize=11, fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Harmonic vs Percussive
        ax5 = fig.add_subplot(gs[3, 2])
        ax5.plot(time_axis, features['harmonic_strength'][0], label='Harmonic', alpha=0.7)
        ax5.plot(time_axis, features['percussive_strength'][0], label='Percussive', alpha=0.7)
        if len(whistle_frames) > 0:
            whistle_times = librosa.frames_to_time(np.array([f[0] for f in whistle_frames]),
                                                  sr=self.sr, hop_length=self.hop_length)
            ax5.scatter(whistle_times, features['harmonic_strength'][0][[f[0] for f in whistle_frames]], 
                       color='green', s=100, marker='^', label='Whistle', zorder=5)
        ax5.set_title('Harmonic vs Percussive', fontsize=11, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Onset Strength
        ax6 = fig.add_subplot(gs[4, 0])
        ax6.plot(time_axis, features['onset_env'], label='Onset Envelope', alpha=0.7, color='orange')
        ax6.set_title('Onset Strength', fontsize=11, fontweight='bold')
        ax6.grid(True, alpha=0.3)
        
        # 7. RMS Energy
        ax7 = fig.add_subplot(gs[4, 1])
        ax7.plot(time_axis, features['rms'][0], label='RMS Energy', alpha=0.7, color='purple')
        ax7.set_title('RMS Energy', fontsize=11, fontweight='bold')
        ax7.grid(True, alpha=0.3)
        
        # 8. Spectral Contrast
        ax8 = fig.add_subplot(gs[4, 2])
        img_contrast = librosa.display.specshow(features['spec_contrast'], sr=self.sr,
                                               hop_length=self.hop_length, x_axis='time', ax=ax8)
        ax8.set_title('Spectral Contrast', fontsize=11, fontweight='bold')
        plt.colorbar(img_contrast, ax=ax8)
        
        # 9. Subband Energy
        ax9 = fig.add_subplot(gs[5, :])
        subband = features['subband_energy']
        for name, energy in subband.items():
            ax9.plot(time_axis[:len(energy)], energy, label=name, alpha=0.7)
        ax9.set_title('Subband Energy Distribution', fontsize=11, fontweight='bold')
        ax9.legend(loc='upper right', ncol=6)
        ax9.grid(True, alpha=0.3)
        
        # 10. Peak-to-Average Ratio
        ax10 = fig.add_subplot(gs[6, 0])
        ax10.plot(time_axis, features['peak_avg_ratio'], label='Peak-Avg Ratio', alpha=0.7, color='brown')
        ax10.set_title('Peak-to-Average Ratio', fontsize=11, fontweight='bold')
        ax10.grid(True, alpha=0.3)
        
        # 11. Chroma Energy
        ax11 = fig.add_subplot(gs[6, 1])
        ax11.plot(time_axis, features['chroma_energy'], label='Chroma Energy', alpha=0.7, color='teal')
        ax11.set_title('Chroma Energy (Pitch)', fontsize=11, fontweight='bold')
        ax11.grid(True, alpha=0.3)
        
        # 12. Spectral Variation
        ax12 = fig.add_subplot(gs[6, 2])
        ax12.plot(time_axis, features['spectral_variation'], label='Spec Variation', alpha=0.7, color='crimson')
        ax12.set_title('Spectral Variation', fontsize=11, fontweight='bold')
        ax12.grid(True, alpha=0.3)
        
        # 13. MFCC
        ax13 = fig.add_subplot(gs[7, :2])
        img_mfcc = librosa.display.specshow(features['mfcc'], sr=self.sr,
                                           hop_length=self.hop_length, x_axis='time', ax=ax13)
        ax13.set_title('MFCC Features', fontsize=11, fontweight='bold')
        plt.colorbar(img_mfcc, ax=ax13)
        
        # 14. Quality Metrics Panel
        ax14 = fig.add_subplot(gs[7, 2])
        ax14.axis('off')
        
        quality_text = f"""
        📊 QUALITY METRICS
        ─────────────────────
        SNR: {quality_metrics['snr_db']:.2f} dB
        Quality: {quality_metrics['audio_quality']}
        
        🔊 DETECTIONS
        ─────────────────────
        Claps: {len(clap_frames)}
        Whistles: {len(whistle_frames)}
        Total: {quality_metrics['num_detections']}
        
        📈 SEGMENTS: {quality_metrics['num_segments']}
        
        ⏱️  TIMING
        ─────────────────────
        """
        
        if quality_metrics['timing_info']:
            timing = quality_metrics['timing_info']
            quality_text += f"Mean Interval: {timing['mean_interval']:.3f}s\n"
            quality_text += f"BPM: {timing['bpm']:.1f}"
        
        ax14.text(0.05, 0.5, quality_text, fontsize=10, family='monospace',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
                 verticalalignment='center')
        
        plt.suptitle('Ultra-Advanced Sound Event Detection - Full Analysis', 
                    fontsize=15, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.show()
        print("✅ Advanced visualization complete")
    
    def save_results_advanced(self, results, output_file="detection_results_advanced.json"):
        """Save comprehensive results to JSON"""
        save_data = {
            'file': results['file'],
            'timestamp': results['timestamp'],
            'duration': len(results['audio']) / self.sr,
            'quality_metrics': {
                'snr_db': float(results['quality_metrics']['snr_db']),
                'audio_quality': results['quality_metrics']['audio_quality'],
                'num_segments': results['quality_metrics']['num_segments'],
                'num_detections': results['quality_metrics']['num_detections']
            },
            'detections': {
                'claps': [
                    {
                        'time': float(t),
                        'confidence': float(results['clap'][i][1] * 100),
                        'frame': int(results['clap'][i][0])
                    }
                    for i, t in enumerate(results['clap_times'])
                ],
                'whistles': [
                    {
                        'time': float(t),
                        'confidence': float(results['whistle'][i][1] * 100),
                        'frame': int(results['whistle'][i][0])
                    }
                    for i, t in enumerate(results['whistle_times'])
                ]
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"✅ Results saved to {output_file}")
    
    def print_advanced_summary(self, results):
        """Print comprehensive detection summary"""
        print("\n" + "="*70)
        print("📋 ULTRA-ADVANCED DETECTION RESULTS")
        print("="*70)
        
        quality = results['quality_metrics']
        
        print(f"\n🎯 AUDIO QUALITY ANALYSIS:")
        print(f"   Signal-to-Noise Ratio: {quality['snr_db']:.2f} dB")
        print(f"   Quality Level: {quality['audio_quality']}")
        print(f"   Audio Segments: {quality['num_segments']}")
        
        print(f"\n🔊 CLAP DETECTIONS: {len(results['clap'])}")
        if len(results['clap']) > 0:
            for i, (clap_data, time) in enumerate(zip(results['clap'], 
                                                       results['clap_times']), 1):
                confidence = clap_data[1] * 100 if isinstance(clap_data, tuple) else 80
                print(f"   Clap {i}: {time:.3f}s | Confidence: {confidence:.1f}%")
        
        print(f"\n🎵 WHISTLE DETECTIONS: {len(results['whistle'])}")
        if len(results['whistle']) > 0:
            for i, (whistle_data, time) in enumerate(zip(results['whistle'], 
                                                         results['whistle_times']), 1):
                confidence = whistle_data[1] * 100 if isinstance(whistle_data, tuple) else 80
                print(f"   Whistle {i}: {time:.3f}s | Confidence: {confidence:.1f}%")
        
        if quality['timing_info']:
            timing = quality['timing_info']
            print(f"\n⏱️  TEMPORAL ANALYSIS:")
            print(f"   Mean Interval: {timing['mean_interval']:.3f}s")
            print(f"   Regular Pattern: {timing['is_regular']}")
            print(f"   BPM: {timing['bpm']:.1f}")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Events: {quality['num_detections']}")
        print(f"   Duration: {len(results['audio'])/self.sr:.2f}s")
        print("="*70 + "\n")
    
    def batch_process(self, file_paths, plot=False, save_results=False):
        """Process multiple audio files"""
        print(f"\n🔄 Batch processing {len(file_paths)} files...")
        all_results = []
        
        for file_path in file_paths:
            print(f"\n▶ Processing: {file_path}")
            result = self.detect(file_path, plot=plot, save_results=save_results)
            if result:
                all_results.append(result)
        
        return all_results
    
    def compare_detections(self, result1, result2):
        """Compare two detection results"""
        print("\n📊 COMPARISON ANALYSIS")
        print("="*70)
        
        clap_diff = len(result1['clap']) - len(result2['clap'])
        whistle_diff = len(result1['whistle']) - len(result2['whistle'])
        
        print(f"File 1: {result1['file']}")
        print(f"File 2: {result2['file']}")
        print(f"\nClap Difference: {clap_diff:+d}")
        print(f"Whistle Difference: {whistle_diff:+d}")
        print(f"SNR Difference: {result1['quality_metrics']['snr_db'] - result2['quality_metrics']['snr_db']:+.2f} dB")


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    
    # Initialize detector
    detector = UltraAdvancedSoundEventDetector(sr=22050)
    
   # Example 1: Single file detection
    print("\n" + "🎯 EXAMPLE 1: Single File Detection")
    # Replace the file name below with the name of the audio file you placed in this directory
    audio_file = "test_events.wav"  
    results = detector.detect(audio_file, plot=True, save_results=True)
    
    # Example 2: Batch processing
    # print("\n" + "🎯 EXAMPLE 2: Batch Processing")
    # audio_files = ["audio1.wav", "audio2.wav", "audio3.wav"]
    # all_results = detector.batch_process(audio_files, plot=False, save_results=True)
    
    # Example 3: Compare two files
    # print("\n" + "🎯 EXAMPLE 3: Comparison")
    # result1 = detector.detect("file1.wav", plot=False)
    # result2 = detector.detect("file2.wav", plot=False)
    # detector.compare_detections(result1, result2)
    
    # Example 4: Get ML-ready features
    # if results:
    #     ml_features = results['ml_features']
    #     print(f"ML Features extracted: {len(ml_features)} frames")
    
    # Example 5: Train custom model
    # if results:
    #     for i, frame_feature in enumerate(results['ml_features']):
    #         detector.model_trainer.add_training_sample(frame_feature, 'clap')
    #     detector.model_trainer.train_simple_model()
    #     detector.model_trainer.save_model("my_sound_model.pkl")
    
    print("\n✨ Detection pipeline complete!")
