import pygame
import math
import random
import sys
import json
import numpy as np
import time

pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)

# Extended vibrant color palette
BRIGHT_RED = (255, 50, 50)
BRIGHT_GREEN = (50, 255, 50)
BRIGHT_BLUE = (50, 50, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
LIME = (191, 255, 0)
TURQUOISE = (64, 224, 208)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
CORAL = (255, 127, 80)
VIOLET = (138, 43, 226)
CRIMSON = (220, 20, 60)
EMERALD = (80, 200, 120)
SAPPHIRE = (15, 82, 186)
NEON_GREEN = (57, 255, 20)
HOT_PINK = (255, 20, 147)
ELECTRIC_BLUE = (125, 249, 255)

FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Asteroids")
clock = pygame.time.Clock()

HIGHSCORE_FILE = "highscore.json"

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.3
        self.sfx_volume = 0.7
        self.music_enabled = True
        self.sfx_enabled = True
        self.background_music = None
        self.create_sounds()
        self.start_background_music()

    def create_sounds(self):
        try:
            self.sounds['shoot'] = self.create_enhanced_laser(600, 0.1)
            self.sounds['explosion'] = self.create_enhanced_explosion(0.4)
            self.sounds['thrust'] = self.create_enhanced_thrust(180, 0.2)
            self.sounds['menu_select'] = self.create_tone(880, 0.05)
            self.sounds['menu_confirm'] = self.create_tone_sweep(440, 880, 0.1)
            self.sounds['shield_activate'] = self.create_shield_sound(0.3)
            self.sounds['coin_collect'] = self.create_coin_sound(0.2)
            self.sounds['powerup'] = self.create_powerup_sound(0.3)
        except:
            # Fallback to simple sounds
            try:
                self.sounds['shoot'] = self.create_simple_tone(440, 0.1)
                self.sounds['explosion'] = self.create_simple_tone(220, 0.3)
                self.sounds['thrust'] = self.create_simple_tone(180, 0.2)
                self.sounds['menu_select'] = self.create_simple_tone(880, 0.05)
                self.sounds['menu_confirm'] = self.create_simple_tone(660, 0.1)
                self.sounds['shield_activate'] = self.create_simple_tone(440, 0.2)
                self.sounds['coin_collect'] = self.create_simple_tone(660, 0.1)
                self.sounds['powerup'] = self.create_simple_tone(880, 0.2)
            except:
                self.sounds = {}

    def create_enhanced_laser(self, frequency, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate
            progress = t / duration

            # Multi-layered laser sound with realistic sci-fi characteristics

            # Main laser frequency with dramatic sweep
            main_freq = frequency * (1.5 - progress * 0.8)  # Frequency drops dramatically
            main_wave = math.sin(main_freq * 2 * math.pi * t)

            # High-frequency zap component
            zap_freq = frequency * 3 + 1000 * math.sin(t * 80)
            zap_wave = 0.3 * math.sin(zap_freq * 2 * math.pi * t)

            # Electric crackle effect
            crackle = 0.1 * random.uniform(-1, 1) * math.exp(-t * 25)

            # Sub-bass thump at the beginning
            bass_freq = 60
            bass_wave = 0.4 * math.sin(bass_freq * 2 * math.pi * t) * math.exp(-t * 30)

            # Sharp attack envelope with quick decay
            envelope = math.exp(-t * 18) * (1 - math.exp(-t * 100))

            # Combine all components
            wave = envelope * (main_wave * 0.6 + zap_wave + crackle + bass_wave)

            # Add slight stereo separation for width
            left_channel = wave * (0.9 + 0.1 * math.sin(t * 40))
            right_channel = wave * (0.9 - 0.1 * math.sin(t * 40))

            wave_value = 4000 * wave
            arr.append([int(wave_value * left_channel), int(wave_value * right_channel)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_enhanced_explosion(self, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate
            progress = t / duration

            # INTENSE multi-layered explosion with maximum impact

            # MASSIVE initial blast - ultra-sharp attack with deep sub-bass
            blast_envelope = math.exp(-t * 18) * (1 - math.exp(-t * 300))
            # Multiple sub-bass frequencies for earth-shaking effect
            sub_bass1 = 1.2 * math.sin(35 * 2 * math.pi * t) * blast_envelope
            sub_bass2 = 0.8 * math.sin(55 * 2 * math.pi * t) * blast_envelope
            sub_bass3 = 0.6 * math.sin(75 * 2 * math.pi * t) * blast_envelope

            # AGGRESSIVE mid-frequency explosion core
            core_envelope = math.exp(-t * 6) * (1 - progress * 0.2)
            core_freq1 = 150 + 80 * math.sin(t * 4)
            core_freq2 = 200 + 60 * math.sin(t * 7)
            core_freq3 = 180 + 100 * math.sin(t * 5)
            explosion_core = 0.9 * (
                math.sin(core_freq1 * 2 * math.pi * t) +
                math.sin(core_freq2 * 2 * math.pi * t) +
                math.sin(core_freq3 * 2 * math.pi * t)
            ) * core_envelope

            # CHAOTIC high-frequency debris field
            debris_envelope = math.exp(-t * 12) * random.uniform(0.7, 1.3)
            # Multiple debris layers for chaos
            debris1 = 0.5 * random.uniform(-1, 1) * debris_envelope
            debris2 = 0.4 * random.uniform(-1, 1) * debris_envelope * math.sin(t * 100)
            debris3 = 0.3 * random.uniform(-1, 1) * debris_envelope * math.sin(t * 200)
            total_debris = debris1 + debris2 + debris3

            # PIERCING metallic shrapnel with multiple frequencies
            shrapnel_envelope = math.exp(-t * 30) * (1 - math.exp(-t * 150))
            shrapnel_freq1 = 2500 + 800 * math.sin(t * 15)
            shrapnel_freq2 = 3200 + 600 * math.sin(t * 20)
            shrapnel_freq3 = 4000 + 400 * math.sin(t * 25)
            metallic_shrapnel = 0.4 * shrapnel_envelope * (
                math.sin(shrapnel_freq1 * 2 * math.pi * t) +
                0.7 * math.sin(shrapnel_freq2 * 2 * math.pi * t) +
                0.5 * math.sin(shrapnel_freq3 * 2 * math.pi * t)
            )

            # VIOLENT air displacement and shockwave
            shockwave_envelope = (1 - progress * 0.5) * math.exp(-t * 3)
            shockwave1 = 0.7 * random.uniform(-1, 1) * shockwave_envelope
            shockwave2 = 0.5 * random.uniform(-1, 1) * shockwave_envelope * math.sin(t * 50)
            total_shockwave = shockwave1 + shockwave2

            # CRACKLING electrical discharge (like from destroyed electronics)
            if t < 0.2:  # Only in first 0.2 seconds
                electrical_envelope = math.exp(-t * 25) * random.uniform(0.8, 1.2)
                electrical_crackle = 0.3 * electrical_envelope * random.choice([-1, 1]) * random.uniform(0.5, 1.0)
            else:
                electrical_crackle = 0

            # SECONDARY explosion resonance
            if t > 0.05 and t < 0.25:  # Secondary blast between 0.05-0.25 seconds
                secondary_t = t - 0.05
                secondary_envelope = math.exp(-secondary_t * 20) * (1 - math.exp(-secondary_t * 100))
                secondary_freq = 90 + 40 * math.sin(secondary_t * 8)
                secondary_blast = 0.6 * math.sin(secondary_freq * 2 * math.pi * secondary_t) * secondary_envelope
            else:
                secondary_blast = 0

            # Combine ALL layers for MAXIMUM IMPACT
            wave = (sub_bass1 + sub_bass2 + sub_bass3 + explosion_core +
                   total_debris + metallic_shrapnel + total_shockwave +
                   electrical_crackle + secondary_blast)

            # AGGRESSIVE dynamic range compression for MASSIVE impact
            wave_abs = abs(wave)
            if wave_abs > 1.0:
                # Hard limiting with saturation
                wave = wave / wave_abs * (1.0 + (wave_abs - 1.0) * 0.1)
            elif wave_abs > 0.8:
                # Soft compression
                compressed_amount = (wave_abs - 0.8) / 0.2
                wave = wave * (0.8 + compressed_amount * 0.15) / wave_abs

            # EXTREME stereo width for immersive destruction
            left_chaos = 0.85 + 0.15 * random.uniform(-1, 1)
            right_chaos = 0.85 + 0.15 * random.uniform(-1, 1)

            # Add slight delay between channels for width
            if i > 5:  # Small delay offset
                delayed_wave = wave * 0.3  # 30% delayed signal
                left_final = wave * left_chaos + delayed_wave * 0.2
                right_final = wave * right_chaos + delayed_wave * 0.2
            else:
                left_final = wave * left_chaos
                right_final = wave * right_chaos

            # MAXIMUM volume for devastating impact
            wave_value = 7500  # Increased from 5000
            arr.append([int(wave_value * left_final), int(wave_value * right_final)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_enhanced_thrust(self, frequency, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate
            progress = t / duration

            # Realistic rocket engine sound with multiple components

            # Main engine burn - low frequency with harmonics
            main_freq = frequency + 20 * math.sin(t * 8)  # Slight frequency variation
            fundamental = 0.4 * math.sin(main_freq * 2 * math.pi * t)

            # Engine harmonics for richness
            harmonic2 = 0.2 * math.sin(main_freq * 2 * 2 * math.pi * t)
            harmonic3 = 0.1 * math.sin(main_freq * 3 * 2 * math.pi * t)

            # Combustion noise - filtered white noise
            combustion_intensity = 0.6 + 0.4 * math.sin(t * 12)
            combustion_noise = combustion_intensity * random.uniform(-0.5, 0.5)

            # High-frequency gas hiss
            hiss_intensity = 0.3 + 0.2 * math.sin(t * 25)
            gas_hiss = hiss_intensity * random.uniform(-0.2, 0.2)

            # Engine vibration - subtle tremolo effect
            vibration_freq = 30 + 10 * math.sin(t * 4)
            vibration = 1 + 0.15 * math.sin(vibration_freq * 2 * math.pi * t)

            # Sub-bass rumble for power feeling
            rumble = 0.3 * math.sin(80 * 2 * math.pi * t) * (0.8 + 0.2 * math.sin(t * 6))

            # Doppler-like pitch modulation
            doppler_mod = 1 + 0.05 * math.sin(t * 15)

            # Combine all engine components
            engine_sound = (fundamental + harmonic2 + harmonic3) * vibration * doppler_mod
            engine_sound += combustion_noise + gas_hiss + rumble

            # Envelope for natural attack and sustain
            envelope = min(1.0, t * 5)  # Quick attack
            if progress > 0.8:  # Fade out in last 20%
                envelope *= (1 - (progress - 0.8) / 0.2)

            wave = engine_sound * envelope

            # Stereo width with engine pan
            left_engine = wave * (0.95 + 0.05 * math.sin(t * 7))
            right_engine = wave * (0.95 - 0.05 * math.sin(t * 7))

            wave_value = 3000
            arr.append([int(wave_value * left_engine), int(wave_value * right_engine)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_tone(self, frequency, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate

            # Clean menu selection tone with subtle character

            # Main tone with slight detuning for warmth
            main_wave = 0.7 * math.sin(frequency * 2 * math.pi * t)
            detune_wave = 0.3 * math.sin(frequency * 1.003 * 2 * math.pi * t)

            # Gentle envelope
            envelope = math.exp(-t * 8) * (1 - math.exp(-t * 30))

            wave = envelope * (main_wave + detune_wave)

            wave_value = 2500
            arr.append([int(wave_value * wave), int(wave_value * wave)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_simple_tone(self, frequency, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = 2000 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            arr.append([int(wave), int(wave)])
        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_tone_sweep(self, start_freq, end_freq, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate
            progress = t / duration

            # Smooth frequency sweep for menu confirm
            freq = start_freq + (end_freq - start_freq) * (progress ** 0.7)  # Curved sweep

            # Main tone with harmonic
            main_wave = 0.7 * math.sin(freq * 2 * math.pi * t)
            harmonic = 0.3 * math.sin(freq * 1.5 * 2 * math.pi * t)

            # Envelope with smooth attack and decay
            envelope = math.sin(progress * math.pi) * math.exp(-progress * 2)

            # Slight vibrato for warmth
            vibrato = 1 + 0.05 * math.sin(8 * 2 * math.pi * t)

            wave = envelope * (main_wave + harmonic) * vibrato

            wave_value = 2800
            arr.append([int(wave_value * wave), int(wave_value * wave)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_shield_sound(self, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate
            progress = t / duration

            # Sci-fi shield activation with multiple layers

            # Power-up sweep
            sweep_freq = 200 + 800 * progress
            sweep_wave = 0.4 * math.sin(sweep_freq * 2 * math.pi * t)

            # Energy crackling
            crackle_intensity = math.exp(-t * 3)
            crackle = 0.2 * crackle_intensity * random.uniform(-1, 1)

            # Harmonic resonance
            harmonic1 = 0.3 * math.sin(400 * 2 * math.pi * t)
            harmonic2 = 0.2 * math.sin(600 * 2 * math.pi * t)

            # Modulation for sci-fi effect
            modulation = 1 + 0.3 * math.sin(25 * 2 * math.pi * t)

            envelope = math.exp(-t * 4) * (1 - math.exp(-t * 20))
            wave = envelope * (sweep_wave + crackle + harmonic1 + harmonic2) * modulation

            wave_value = 3500
            arr.append([int(wave_value * wave), int(wave_value * wave)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_coin_sound(self, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate

            # Pleasant coin collection sound with multiple tones

            # Main bell-like tone
            main_freq = 880
            main_wave = 0.5 * math.sin(main_freq * 2 * math.pi * t)

            # Harmonic overtones for richness
            overtone1 = 0.3 * math.sin(main_freq * 1.5 * 2 * math.pi * t)
            overtone2 = 0.2 * math.sin(main_freq * 2 * 2 * math.pi * t)
            overtone3 = 0.1 * math.sin(main_freq * 3 * 2 * math.pi * t)

            # Quick bright sparkle at the beginning
            sparkle_freq = 1760 + 500 * math.sin(t * 60)
            sparkle_envelope = math.exp(-t * 25)
            sparkle = 0.2 * sparkle_envelope * math.sin(sparkle_freq * 2 * math.pi * t)

            # Main envelope with natural decay
            envelope = math.exp(-t * 12) * (1 - math.exp(-t * 50))

            wave = envelope * (main_wave + overtone1 + overtone2 + overtone3 + sparkle)

            wave_value = 3000
            arr.append([int(wave_value * wave), int(wave_value * wave)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_powerup_sound(self, duration):
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            t = i / sample_rate
            progress = t / duration

            # Epic power-up sound with rising energy

            # Main rising sweep
            sweep_freq = 220 * (2 ** (progress * 2.5))  # More dramatic rise
            main_wave = 0.6 * math.sin(sweep_freq * 2 * math.pi * t)

            # Harmonic layers for richness
            harmonic1 = 0.3 * math.sin(sweep_freq * 1.5 * 2 * math.pi * t)
            harmonic2 = 0.2 * math.sin(sweep_freq * 2 * 2 * math.pi * t)

            # Energy burst at the end
            if progress > 0.7:
                burst_intensity = (progress - 0.7) / 0.3
                energy_burst = 0.4 * burst_intensity * math.sin(1760 * 2 * math.pi * t)
                main_wave += energy_burst

            # Modulation for sci-fi character
            modulation = 1 + 0.2 * math.sin(15 * 2 * math.pi * t)

            # Dynamic envelope
            envelope = (1 - progress * 0.3) * (1 - math.exp(-t * 8))
            if progress > 0.8:  # Final crescendo
                envelope *= 1 + (progress - 0.8) * 2

            wave = envelope * (main_wave + harmonic1 + harmonic2) * modulation

            wave_value = 3500
            arr.append([int(wave_value * wave), int(wave_value * wave)])

        sound_array = np.array(arr, dtype=np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def create_background_music(self):
        sample_rate = 44100
        duration = 45  # Longer loop for more variety
        frames = int(duration * sample_rate)
        arr = []

        # Extended chord progression in A minor with more sophisticated harmony
        chord_progression = [
            ([220, 262, 330], [110, 165]),    # A minor + bass
            ([294, 349, 440], [147, 220]),    # D minor + bass
            ([262, 311, 392], [131, 196]),    # C major + bass
            ([349, 415, 523], [174, 261]),    # F major + bass
            ([247, 294, 370], [123, 185]),    # B diminished + bass
            ([330, 392, 494], [165, 247]),    # E minor + bass
            ([294, 370, 440], [147, 220]),    # D minor + bass
            ([220, 277, 330], [110, 165]),    # A minor + bass
        ]

        for i in range(frames):
            t = i / sample_rate

            # Current chord (changes every 5.625 seconds)
            chord_index = int(t / 5.625) % len(chord_progression)
            chord_notes, bass_notes = chord_progression[chord_index]

            wave = 0

            # Bass line with subtle movement
            bass_envelope = 0.4 * (1 + 0.2 * math.sin(t * 0.3))
            for bass_freq in bass_notes:
                bass_wave = bass_envelope * math.sin(bass_freq * 2 * math.pi * t)
                bass_wave += 0.1 * math.sin(bass_freq * 2 * 2 * math.pi * t)  # Octave harmonic
                wave += bass_wave

            # Main chord pad with gentle tremolo
            pad_envelope = 0.25 * (1 + 0.15 * math.sin(t * 0.8))
            for freq in chord_notes:
                # Main tone
                pad_wave = pad_envelope * math.sin(freq * 2 * math.pi * t)
                # Add slight detuning for warmth
                pad_wave += pad_envelope * 0.3 * math.sin(freq * 1.002 * 2 * math.pi * t)
                wave += pad_wave

            # Ethereal high melody that appears periodically
            if (t % 22.5) > 11.25:  # Play melody in second half of each section
                melody_envelope = 0.15 * math.sin((t % 11.25) / 11.25 * math.pi)
                melody_freq = chord_notes[0] * 2  # Octave above root
                if chord_index % 2 == 1:  # Alternate melody notes
                    melody_freq = chord_notes[1] * 2
                melody_wave = melody_envelope * math.sin(melody_freq * 2 * math.pi * t)
                # Add subtle vibrato
                vibrato = 1 + 0.05 * math.sin(6 * 2 * math.pi * t)
                melody_wave *= vibrato
                wave += melody_wave

            # Ambient space texture with filtered noise
            if t > 10:  # Start ambient texture after 10 seconds
                ambient_intensity = 0.05 * (1 + 0.5 * math.sin(t * 0.1))
                ambient_noise = ambient_intensity * random.uniform(-1, 1)
                # Apply simple low-pass filter effect
                if i > 0:
                    ambient_noise = 0.7 * ambient_noise + 0.3 * previous_ambient
                wave += ambient_noise
                previous_ambient = ambient_noise
            else:
                previous_ambient = 0

            # Subtle arpeggiation effect
            arp_time = (t * 2) % 1
            if arp_time < 0.1:  # Brief arp notes
                arp_note = chord_notes[int((t * 2) % len(chord_notes))]
                arp_envelope = 0.1 * math.exp(-arp_time * 20)
                arp_wave = arp_envelope * math.sin(arp_note * 4 * 2 * math.pi * t)
                wave += arp_wave

            # Overall envelope for smooth looping
            loop_envelope = 1.0
            if t < 2:  # Fade in
                loop_envelope = t / 2
            elif t > duration - 2:  # Fade out
                loop_envelope = (duration - t) / 2

            wave *= loop_envelope

            # Stereo width with subtle panning
            left_pan = 0.95 + 0.05 * math.sin(t * 0.7)
            right_pan = 0.95 - 0.05 * math.sin(t * 0.7)

            wave_value = 1200  # Lower volume for background music
            arr.append([int(wave_value * wave * left_pan), int(wave_value * wave * right_pan)])

        sound_array = np.array(arr, dtype=np.int16)
        return pygame.sndarray.make_sound(sound_array)

    def start_background_music(self):
        if self.music_enabled:
            try:
                if not self.background_music:
                    self.background_music = self.create_background_music()
                self.background_music.set_volume(self.music_volume)
                self.background_music.play(-1)
            except:
                pass

    def stop_background_music(self):
        if self.background_music:
            self.background_music.stop()

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        if self.background_music:
            self.background_music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(1, volume))

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.start_background_music()
        else:
            self.stop_background_music()

    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled

    def play(self, sound_name):
        if self.sfx_enabled and sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(self.sfx_volume)
                sound.play()
            except:
                pass

class Particle:
    def __init__(self, x, y, vel_x, vel_y, color=WHITE, life=30):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.life = life
        self.max_life = life
        self.size = random.uniform(1, 4)  # Variable particle sizes
        self.trail_positions = [(x, y)]  # Trail effect

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        self.vel_x *= 0.98
        self.vel_y *= 0.98

        # Screen wrapping for particles
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT

        # Update trail
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > 5:  # Keep last 5 positions
            self.trail_positions.pop(0)

    def draw(self, screen):
        if self.life > 0:
            life_ratio = self.life / self.max_life

            # Draw trail effect
            for i, (trail_x, trail_y) in enumerate(self.trail_positions[:-1]):
                trail_alpha = life_ratio * (i / len(self.trail_positions)) * 0.5
                trail_color = tuple(int(c * trail_alpha) for c in self.color)
                if sum(trail_color) > 0:  # Only draw if visible
                    pygame.draw.circle(screen, trail_color, (int(trail_x), int(trail_y)), max(1, int(self.size * 0.5)))

            # Main particle with pulsing effect
            pulse = 0.8 + 0.2 * math.sin(time.time() * 10)
            main_color = tuple(int(c * life_ratio * pulse) for c in self.color)

            # Draw main particle
            pygame.draw.circle(screen, main_color, (int(self.x), int(self.y)), int(self.size))

            # Add bright center for some particles
            if life_ratio > 0.5 and self.size > 2:
                center_color = tuple(min(255, int(c * 1.5)) for c in main_color)
                pygame.draw.circle(screen, center_color, (int(self.x), int(self.y)), max(1, int(self.size * 0.4)))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        self.size = 10
        self.thrust = 0.2
        self.friction = 0.98
        self.max_speed = 8
        self.thrusting = False
        self.invulnerable_time = 0
        self.max_invulnerable_time = 120
        self.shield_active = False
        self.shield_time = 0
        self.rapid_fire_cooldown = 0

    def update(self, sound_manager, speed_boost_level=0):
        keys = pygame.key.get_pressed()
        self.thrusting = False

        rotation_speed = 5 + speed_boost_level
        if keys[pygame.K_LEFT]:
            self.angle -= rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += rotation_speed

        if keys[pygame.K_UP]:
            self.thrusting = True
            thrust_power = self.thrust + (speed_boost_level * 0.1)
            thrust_x = math.cos(math.radians(self.angle)) * thrust_power
            thrust_y = math.sin(math.radians(self.angle)) * thrust_power
            self.vel_x += thrust_x
            self.vel_y += thrust_y
            if random.random() < 0.1:
                sound_manager.play('thrust')

        max_speed = self.max_speed + (speed_boost_level * 2)
        speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
        if speed > max_speed:
            self.vel_x = (self.vel_x / speed) * max_speed
            self.vel_y = (self.vel_y / speed) * max_speed

        self.vel_x *= self.friction
        self.vel_y *= self.friction

        self.x += self.vel_x
        self.y += self.vel_y

        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT

        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1

        if self.shield_time > 0:
            self.shield_time -= 1
            self.shield_active = True
        else:
            self.shield_active = False

        if self.rapid_fire_cooldown > 0:
            self.rapid_fire_cooldown -= 1

    def draw(self, screen, ship_skin='default'):
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 < 5:
            return

        points = []
        if ship_skin == 'astro':
            ship_points = [(-8, -10), (20, 0), (-8, 10), (-3, 8), (-3, -8)]
            color = BLUE
        elif ship_skin == 'fighter':
            ship_points = [(-12, -6), (18, 0), (-12, 6), (-8, 4), (-8, -4)]
            color = RED
        elif ship_skin == 'stealth':
            ship_points = [(-5, -15), (18, -2), (14, 0), (18, 2), (-5, 15), (-8, 8), (-12, 0), (-8, -8)]
            color = (80, 80, 120)
        elif ship_skin == 'classic':
            ship_points = [(-8, -12), (16, 0), (-8, 12), (-4, 0)]
            color = GREEN
        else:
            ship_points = [(-10, -8), (15, 0), (-10, 8), (-5, 0)]
            color = WHITE

        for point in ship_points:
            rotated_x = point[0] * math.cos(math.radians(self.angle)) - point[1] * math.sin(math.radians(self.angle))
            rotated_y = point[0] * math.sin(math.radians(self.angle)) + point[1] * math.cos(math.radians(self.angle))
            points.append((self.x + rotated_x, self.y + rotated_y))

        pygame.draw.polygon(screen, color, points)

        if ship_skin == 'astro':
            center_x = self.x + math.cos(math.radians(self.angle)) * 5
            center_y = self.y + math.sin(math.radians(self.angle)) * 5
            pygame.draw.circle(screen, YELLOW, (int(center_x), int(center_y)), 3)
        elif ship_skin == 'fighter':
            wing_points = [(-8, -10), (-4, -8), (-8, -6)]
            wing_points2 = [(-8, 6), (-4, 8), (-8, 10)]
            for wing in [wing_points, wing_points2]:
                rotated_wing = []
                for point in wing:
                    rotated_x = point[0] * math.cos(math.radians(self.angle)) - point[1] * math.sin(math.radians(self.angle))
                    rotated_y = point[0] * math.sin(math.radians(self.angle)) + point[1] * math.cos(math.radians(self.angle))
                    rotated_wing.append((self.x + rotated_x, self.y + rotated_y))
                pygame.draw.polygon(screen, YELLOW, rotated_wing)
        elif ship_skin == 'stealth':
            # Add stealth details - angular lines
            detail_points = [(-2, -8), (8, -4), (8, 4), (-2, 8)]
            rotated_details = []
            for point in detail_points:
                rotated_x = point[0] * math.cos(math.radians(self.angle)) - point[1] * math.sin(math.radians(self.angle))
                rotated_y = point[0] * math.sin(math.radians(self.angle)) + point[1] * math.cos(math.radians(self.angle))
                rotated_details.append((self.x + rotated_x, self.y + rotated_y))
            pygame.draw.polygon(screen, (40, 40, 60), rotated_details)

        if self.shield_active:
            # Pulsing shield effect with multiple colors
            shield_pulse = 0.7 + 0.3 * math.sin(time.time() * 8)

            # Outer shield ring
            outer_color = tuple(int(c * shield_pulse) for c in CYAN)
            pygame.draw.circle(screen, outer_color, (int(self.x), int(self.y)), 22, 3)

            # Middle shield ring
            mid_color = tuple(int(c * shield_pulse * 0.8) for c in ELECTRIC_BLUE)
            pygame.draw.circle(screen, mid_color, (int(self.x), int(self.y)), 20, 2)

            # Inner shield sparkle
            inner_color = tuple(int(c * shield_pulse * 0.6) for c in WHITE)
            pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), 18, 1)

    def get_thrust_particles(self):
        if self.thrusting:
            particles = []
            for _ in range(5):  # More particles
                thrust_angle = self.angle + 180 + random.uniform(-40, 40)
                vel_x = math.cos(math.radians(thrust_angle)) * random.uniform(3, 6)
                vel_y = math.sin(math.radians(thrust_angle)) * random.uniform(3, 6)

                # Colorful engine exhaust
                thrust_colors = [
                    YELLOW, ORANGE, BRIGHT_RED, WHITE,
                    HOT_PINK, ELECTRIC_BLUE, GOLD, CRIMSON
                ]
                color = random.choice(thrust_colors)

                particles.append(Particle(
                    self.x - math.cos(math.radians(self.angle)) * 12,
                    self.y - math.sin(math.radians(self.angle)) * 12,
                    vel_x, vel_y, color, random.randint(15, 25)
                ))

            # Add some special blue core particles
            for _ in range(2):
                thrust_angle = self.angle + 180 + random.uniform(-20, 20)
                vel_x = math.cos(math.radians(thrust_angle)) * random.uniform(2, 4)
                vel_y = math.sin(math.radians(thrust_angle)) * random.uniform(2, 4)
                particles.append(Particle(
                    self.x - math.cos(math.radians(self.angle)) * 8,
                    self.y - math.sin(math.radians(self.angle)) * 8,
                    vel_x, vel_y, ELECTRIC_BLUE, 30
                ))

            return particles
        return []

    def reset_position(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = 0
        self.vel_y = 0
        self.angle = 0
        self.invulnerable_time = self.max_invulnerable_time

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vel_x = math.cos(math.radians(angle)) * 10
        self.vel_y = math.sin(math.radians(angle)) * 10
        self.life = 60
        self.max_life = 60
        self.trail_positions = [(x, y)]

        # Colorful bullets
        self.bullet_colors = [
            CYAN, MAGENTA, YELLOW, NEON_GREEN,
            HOT_PINK, ELECTRIC_BLUE, ORANGE, LIME,
            GOLD, VIOLET, BRIGHT_RED, WHITE
        ]
        self.color = random.choice(self.bullet_colors)
        self.pulse_offset = random.uniform(0, math.pi * 2)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT
        self.life -= 1

        # Update trail
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > 8:  # Longer trail than particles
            self.trail_positions.pop(0)

    def draw(self, screen):
        # Draw colorful trail
        for i, (trail_x, trail_y) in enumerate(self.trail_positions[:-1]):
            trail_alpha = (i / len(self.trail_positions)) * 0.8
            trail_color = tuple(int(c * trail_alpha) for c in self.color)
            if sum(trail_color) > 0:
                trail_size = max(1, int(3 * trail_alpha))
                pygame.draw.circle(screen, trail_color, (int(trail_x), int(trail_y)), trail_size)

        # Main bullet with pulsing glow
        pulse = 0.7 + 0.3 * math.sin(time.time() * 15 + self.pulse_offset)
        main_color = tuple(int(c * pulse) for c in self.color)

        # Draw main bullet with glow effect
        pygame.draw.circle(screen, main_color, (int(self.x), int(self.y)), 3)

        # Bright center
        center_color = tuple(min(255, int(c * 1.3)) for c in main_color)
        pygame.draw.circle(screen, center_color, (int(self.x), int(self.y)), 2)

        # Outer glow
        glow_color = tuple(int(c * 0.4) for c in self.color)
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), 5, 1)

class Asteroid:
    def __init__(self, x, y, size=3):
        self.x = x
        self.y = y
        self.size = size
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.radius = 20 + size * 10
        self.shape_points = self.generate_shape()

        # Colorful asteroid varieties
        self.asteroid_colors = [
            CORAL, TURQUOISE, VIOLET, EMERALD, GOLD,
            ORANGE, PINK, LIME, CYAN, MAGENTA,
            BRIGHT_RED, BRIGHT_BLUE, HOT_PINK, NEON_GREEN,
            CRIMSON, SAPPHIRE, ELECTRIC_BLUE, PURPLE
        ]
        self.color = random.choice(self.asteroid_colors)

        # Add some asteroids with special glow effects
        self.glow_intensity = random.uniform(0.5, 1.0)
        self.pulse_speed = random.uniform(2, 6)

    def generate_shape(self):
        points = []
        num_points = 8
        for i in range(num_points):
            angle = (360 / num_points) * i
            radius_variation = random.uniform(0.7, 1.3)
            points.append((angle, radius_variation))
        return points

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.angle += self.rotation_speed

        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT

    def draw(self, screen):
        import time
        points = []
        for angle_offset, radius_variation in self.shape_points:
            angle = angle_offset + self.angle
            actual_radius = radius_variation * self.radius
            point_x = self.x + math.cos(math.radians(angle)) * actual_radius
            point_y = self.y + math.sin(math.radians(angle)) * actual_radius
            points.append((point_x, point_y))

        # Pulsing glow effect
        pulse = self.glow_intensity * (0.8 + 0.2 * math.sin(time.time() * self.pulse_speed))

        # Main asteroid body with vibrant color
        main_color = tuple(int(c * pulse) for c in self.color)
        pygame.draw.polygon(screen, main_color, points, 3)

        # Inner glow effect
        if self.size >= 2:  # Only larger asteroids get inner glow
            inner_points = []
            for angle_offset, radius_variation in self.shape_points:
                angle = angle_offset + self.angle
                actual_radius = radius_variation * self.radius * 0.6
                point_x = self.x + math.cos(math.radians(angle)) * actual_radius
                point_y = self.y + math.sin(math.radians(angle)) * actual_radius
                inner_points.append((point_x, point_y))

            # Bright inner color
            inner_color = tuple(min(255, int(c * 1.3)) for c in main_color)
            pygame.draw.polygon(screen, inner_color, inner_points, 2)

        # Outer glow rings for extra large asteroids
        if self.size >= 3:
            glow_color = tuple(int(c * 0.3) for c in self.color)
            pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), int(self.radius * 1.2), 1)
            pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), int(self.radius * 1.4), 1)

    def get_explosion_particles(self):
        particles = []
        for _ in range(10 + self.size * 8):  # More particles
            vel_x = random.uniform(-8, 8)  # Faster particles
            vel_y = random.uniform(-8, 8)

            # Use asteroid's color scheme plus some extras
            explosion_colors = [
                self.color,
                tuple(min(255, c + 50) for c in self.color),  # Brighter version
                WHITE, YELLOW, ORANGE, BRIGHT_RED,
                GOLD, ELECTRIC_BLUE, HOT_PINK, NEON_GREEN
            ]
            color = random.choice(explosion_colors)

            # Longer-lasting particles with variety
            life = random.randint(30, 60)
            particles.append(Particle(self.x, self.y, vel_x, vel_y, color, life))

        # Add some special sparkle particles
        for _ in range(5):
            vel_x = random.uniform(-3, 3)
            vel_y = random.uniform(-3, 3)
            sparkle_colors = [GOLD, SILVER, WHITE, CYAN, MAGENTA, YELLOW]
            color = random.choice(sparkle_colors)
            particles.append(Particle(self.x, self.y, vel_x, vel_y, color, 80))

        return particles

def check_collision(obj1_x, obj1_y, obj1_radius, obj2_x, obj2_y, obj2_radius):
    distance = math.sqrt((obj1_x - obj2_x)**2 + (obj1_y - obj2_y)**2)
    return distance < (obj1_radius + obj2_radius)

def load_game_data():
    try:
        with open(HIGHSCORE_FILE, 'r') as f:
            data = json.load(f)
            return {
                'high_score': data.get('high_score', 0),
                'coins': data.get('coins', 0),
                'ship_skin': data.get('ship_skin', 'default'),
                'multi_shot_level': data.get('multi_shot_level', 0),
                'shield_level': data.get('shield_level', 0),
                'rapid_fire_level': data.get('rapid_fire_level', 0),
                'speed_boost_level': data.get('speed_boost_level', 0),
                'owned_ships': data.get('owned_ships', ['default'])
            }
    except:
        return {
            'high_score': 0,
            'coins': 0,
            'ship_skin': 'default',
            'multi_shot_level': 0,
            'shield_level': 0,
            'rapid_fire_level': 0,
            'speed_boost_level': 0,
            'owned_ships': ['default']
        }

def save_game_data(data):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

def spawn_asteroids(num_asteroids, player):
    asteroids = []
    for _ in range(num_asteroids):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if math.sqrt((x - player.x)**2 + (y - player.y)**2) > 100:
                asteroids.append(Asteroid(x, y))
                break
    return asteroids

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3
    SHOP = 4
    SHIP_SELECT = 5
    NEW_GAME_CONFIRM = 6
    SOUND_SETTINGS = 7

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2.5)

        # Colorful stars
        star_colors = [
            WHITE, CYAN, GOLD, PINK, LIME,
            ELECTRIC_BLUE, CORAL, VIOLET, SILVER,
            TURQUOISE, HOT_PINK, NEON_GREEN
        ]
        self.color = random.choice(star_colors)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(1, 4)
        self.twinkle_offset = random.uniform(0, math.pi * 2)

    def draw(self, screen):
        # Twinkling effect
        twinkle = 0.6 + 0.4 * math.sin(time.time() * self.twinkle_speed + self.twinkle_offset)
        current_brightness = self.brightness * twinkle

        # Draw star with twinkling color
        star_color = tuple(int(c * current_brightness) for c in self.color)
        pygame.draw.circle(screen, star_color, (int(self.x), int(self.y)), int(self.size))

        # Add sparkle effect for larger stars
        if self.size > 1.8:
            sparkle_color = tuple(min(255, int(c * 1.3)) for c in star_color)
            pygame.draw.circle(screen, sparkle_color, (int(self.x), int(self.y)), max(1, int(self.size * 0.4)))

def create_starfield(num_stars=150):
    return [Star() for _ in range(num_stars)]

def draw_starfield(screen, stars):
    for star in stars:
        star.draw(screen)

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main():
    sound_manager = SoundManager()
    player = Player(WIDTH // 2, HEIGHT // 2)
    bullets = []
    asteroids = spawn_asteroids(3, player)
    particles = []
    score = 0
    lives = 3
    game_data = load_game_data()
    high_score = game_data['high_score']
    coins = game_data['coins']
    ship_skin = game_data['ship_skin']
    multi_shot_level = game_data['multi_shot_level']
    shield_level = game_data['shield_level']
    rapid_fire_level = game_data['rapid_fire_level']
    speed_boost_level = game_data['speed_boost_level']
    owned_ships = game_data['owned_ships']
    game_state = GameState.MENU
    font = pygame.font.Font(None, 36)
    shop_selection = 0
    ship_selection = 0
    sound_selection = 0

    # Create colorful starfield background
    stars = create_starfield(200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        sound_manager.play('menu_confirm')
                        game_state = GameState.PLAYING
                    elif event.key == pygame.K_s:
                        sound_manager.play('menu_select')
                        game_state = GameState.SHOP
                        shop_selection = 0
                    elif event.key == pygame.K_h:
                        sound_manager.play('menu_select')
                        game_state = GameState.SHIP_SELECT
                        ship_selection = 0
                    elif event.key == pygame.K_n:
                        sound_manager.play('menu_select')
                        game_state = GameState.NEW_GAME_CONFIRM
                    elif event.key == pygame.K_o:
                        sound_manager.play('menu_select')
                        game_state = GameState.SOUND_SETTINGS
                elif game_state == GameState.SHOP:
                    if event.key == pygame.K_ESCAPE:
                        game_state = GameState.MENU
                    elif event.key == pygame.K_UP:
                        sound_manager.play('menu_select')
                        shop_selection = (shop_selection - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        sound_manager.play('menu_select')
                        shop_selection = (shop_selection + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        purchased = False
                        if shop_selection == 0 and coins >= 300 and multi_shot_level == 0:
                            coins -= 300
                            multi_shot_level = 1
                            purchased = True
                        elif shop_selection == 1 and coins >= 800 and multi_shot_level == 1:
                            coins -= 800
                            multi_shot_level = 2
                            purchased = True
                        elif shop_selection == 2 and coins >= 500 and shield_level == 0:
                            coins -= 500
                            shield_level = 1
                            purchased = True
                        elif shop_selection == 3 and coins >= 350 and rapid_fire_level == 0:
                            coins -= 350
                            rapid_fire_level = 1
                            purchased = True

                        if purchased:
                            sound_manager.play('powerup')
                            game_data['coins'] = coins
                            game_data['multi_shot_level'] = multi_shot_level
                            game_data['shield_level'] = shield_level
                            game_data['rapid_fire_level'] = rapid_fire_level
                            save_game_data(game_data)
                elif game_state == GameState.SHIP_SELECT:
                    if event.key == pygame.K_ESCAPE:
                        game_state = GameState.MENU
                    elif event.key == pygame.K_UP:
                        sound_manager.play('menu_select')
                        ship_selection = (ship_selection - 1) % len(owned_ships)
                    elif event.key == pygame.K_DOWN:
                        sound_manager.play('menu_select')
                        ship_selection = (ship_selection + 1) % len(owned_ships)
                    elif event.key == pygame.K_RETURN:
                        sound_manager.play('menu_confirm')
                        ship_skin = owned_ships[ship_selection]
                        game_data['ship_skin'] = ship_skin
                        save_game_data(game_data)
                    elif event.key == pygame.K_b:
                        ship_names = ['astro', 'fighter', 'stealth', 'classic']
                        prices = [500, 750, 600, 400]
                        for i, (ship_name, price) in enumerate(zip(ship_names, prices)):
                            if ship_name not in owned_ships and coins >= price:
                                sound_manager.play('powerup')
                                coins -= price
                                owned_ships.append(ship_name)
                                game_data['coins'] = coins
                                game_data['owned_ships'] = owned_ships
                                save_game_data(game_data)
                                break
                elif game_state == GameState.SOUND_SETTINGS:
                    if event.key == pygame.K_ESCAPE:
                        game_state = GameState.MENU
                    elif event.key == pygame.K_UP:
                        sound_manager.play('menu_select')
                        sound_selection = (sound_selection - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        sound_manager.play('menu_select')
                        sound_selection = (sound_selection + 1) % 4
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if sound_selection == 0:  # Music Volume
                            change = 0.1 if event.key == pygame.K_RIGHT else -0.1
                            new_volume = sound_manager.music_volume + change
                            sound_manager.set_music_volume(new_volume)
                        elif sound_selection == 1:  # SFX Volume
                            change = 0.1 if event.key == pygame.K_RIGHT else -0.1
                            new_volume = sound_manager.sfx_volume + change
                            sound_manager.set_sfx_volume(new_volume)
                        elif sound_selection == 2:  # Toggle Music
                            sound_manager.toggle_music()
                        elif sound_selection == 3:  # Toggle SFX
                            sound_manager.toggle_sfx()
                        sound_manager.play('menu_select')
                elif game_state == GameState.NEW_GAME_CONFIRM:
                    if event.key == pygame.K_y:
                        # Reset all game data except high score
                        high_score_backup = high_score
                        game_data = {
                            'high_score': high_score_backup,
                            'coins': 0,
                            'ship_skin': 'default',
                            'multi_shot_level': 0,
                            'shield_level': 0,
                            'rapid_fire_level': 0,
                            'speed_boost_level': 0,
                            'owned_ships': ['default']
                        }
                        save_game_data(game_data)

                        # Reset local variables
                        coins = 0
                        ship_skin = 'default'
                        multi_shot_level = 0
                        shield_level = 0
                        rapid_fire_level = 0
                        speed_boost_level = 0
                        owned_ships = ['default']
                        score = 0
                        lives = 3

                        # Reset player and game objects
                        player = Player(WIDTH // 2, HEIGHT // 2)
                        bullets = []
                        asteroids = spawn_asteroids(3, player)
                        particles = []

                        game_state = GameState.MENU
                    elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        game_state = GameState.MENU
                elif game_state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        if rapid_fire_level == 0 or player.rapid_fire_cooldown <= 0:
                            if multi_shot_level == 0:
                                bullet = Bullet(player.x, player.y, player.angle)
                                bullets.append(bullet)
                            elif multi_shot_level == 1:
                                for angle_offset in [-15, 0, 15]:
                                    bullet = Bullet(player.x, player.y, player.angle + angle_offset)
                                    bullets.append(bullet)
                            elif multi_shot_level == 2:
                                for angle_offset in [-20, -10, 0, 10, 20]:
                                    bullet = Bullet(player.x, player.y, player.angle + angle_offset)
                                    bullets.append(bullet)
                            sound_manager.play('shoot')
                            if rapid_fire_level > 0:
                                player.rapid_fire_cooldown = max(1, 10 - rapid_fire_level * 5)
                    elif event.key == pygame.K_x and shield_level > 0 and not player.shield_active:
                        player.shield_time = 180
                        player.shield_active = True
                        sound_manager.play('shield_activate')
                    elif event.key == pygame.K_p:
                        game_state = GameState.PAUSED
                elif game_state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        game_state = GameState.PLAYING
                elif game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        player = Player(WIDTH // 2, HEIGHT // 2)
                        bullets = []
                        asteroids = spawn_asteroids(3, player)
                        particles = []
                        score = 0
                        lives = 3
                        game_state = GameState.PLAYING
                    elif event.key == pygame.K_m:
                        game_state = GameState.MENU

        if game_state == GameState.PLAYING:
            player.update(sound_manager, speed_boost_level)
            particles.extend(player.get_thrust_particles())

            for bullet in bullets[:]:
                bullet.update()
                if bullet.life <= 0:
                    bullets.remove(bullet)

            for asteroid in asteroids:
                asteroid.update()

            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)

            for bullet in bullets[:]:
                for asteroid in asteroids[:]:
                    if check_collision(bullet.x, bullet.y, 2, asteroid.x, asteroid.y, asteroid.radius):
                        bullets.remove(bullet)
                        particles.extend(asteroid.get_explosion_particles())
                        asteroids.remove(asteroid)
                        sound_manager.play('explosion')
                        sound_manager.play('coin_collect')
                        score += 100 * asteroid.size
                        coins += 3 * asteroid.size

                        if asteroid.size > 1:
                            for _ in range(2):
                                new_asteroid = Asteroid(
                                    asteroid.x + random.uniform(-20, 20),
                                    asteroid.y + random.uniform(-20, 20),
                                    asteroid.size - 1
                                )
                                asteroids.append(new_asteroid)
                        break

            if player.invulnerable_time == 0 and not player.shield_active:
                for asteroid in asteroids:
                    if check_collision(player.x, player.y, player.size, asteroid.x, asteroid.y, asteroid.radius):
                        lives -= 1
                        sound_manager.play('explosion')
                        particles.extend(asteroid.get_explosion_particles())
                        player.reset_position()

                        if lives <= 0:
                            if score > high_score:
                                high_score = score
                            game_data['high_score'] = high_score
                            game_data['coins'] = coins
                            save_game_data(game_data)
                            game_state = GameState.GAME_OVER
                        break

            if not asteroids:
                asteroids = spawn_asteroids(3 + score // 1500, player)

        screen.fill(BLACK)

        # Draw colorful starfield background for all game states
        draw_starfield(screen, stars)

        if game_state == GameState.PLAYING or game_state == GameState.PAUSED:
            player.draw(screen, ship_skin)

            for bullet in bullets:
                bullet.draw(screen)

            for asteroid in asteroids:
                asteroid.draw(screen)

            for particle in particles:
                particle.draw(screen)

            # Colorful and enhanced UI elements
            score_text = font.render(f"Score: {score}", True, ELECTRIC_BLUE)
            screen.blit(score_text, (10, 10))

            # Color-coded lives indicator
            if lives >= 3:
                lives_color = BRIGHT_GREEN
            elif lives == 2:
                lives_color = YELLOW
            else:
                lives_color = BRIGHT_RED

            lives_text = font.render(f"Lives: {lives}", True, lives_color)
            screen.blit(lives_text, (10, 50))

            # Draw health bar visualization
            bar_width = 100
            bar_height = 8
            bar_x = 10
            bar_y = 75

            # Background bar
            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

            # Health bar segments
            segment_width = bar_width // 3
            for i in range(lives):
                if i == 0:
                    segment_color = BRIGHT_GREEN if lives >= 3 else (YELLOW if lives == 2 else BRIGHT_RED)
                elif i == 1:
                    segment_color = BRIGHT_GREEN if lives >= 2 else YELLOW
                else:
                    segment_color = BRIGHT_GREEN

                pygame.draw.rect(screen, segment_color,
                               (bar_x + i * segment_width + 2, bar_y + 2, segment_width - 4, bar_height - 4))

            high_score_text = font.render(f"High Score: {high_score}", True, GOLD)
            screen.blit(high_score_text, (10, 100))

            coins_text = font.render(f"Coins: {coins}", True, BRIGHT_GREEN)
            screen.blit(coins_text, (10, 130))

            # Add shield indicator
            if player.shield_active:
                shield_text = font.render("SHIELD ACTIVE", True, CYAN)
                screen.blit(shield_text, (WIDTH - 150, 10))

                # Shield timer bar
                shield_ratio = player.shield_time / 180
                shield_bar_width = 120
                shield_bar_height = 6
                pygame.draw.rect(screen, (40, 40, 40), (WIDTH - 140, 35, shield_bar_width, shield_bar_height))
                pygame.draw.rect(screen, CYAN, (WIDTH - 138, 37, int(shield_bar_width * shield_ratio - 4), shield_bar_height - 4))

            if game_state == GameState.PAUSED:
                draw_text(screen, "PAUSED", 72, WIDTH//2, HEIGHT//2, YELLOW)
                draw_text(screen, "Press P to resume", 36, WIDTH//2, HEIGHT//2 + 50, WHITE)

        elif game_state == GameState.MENU:
            draw_text(screen, "ASTEROIDS", 96, WIDTH//2, HEIGHT//2 - 100, WHITE)
            draw_text(screen, "Enhanced Edition", 36, WIDTH//2, HEIGHT//2 - 60, YELLOW)

            draw_text(screen, "CONTROLS:", 36, WIDTH//2, HEIGHT//2 - 10, GREEN)
            draw_text(screen, "Arrow Keys - Move & Rotate", 28, WIDTH//2, HEIGHT//2 + 20, WHITE)
            draw_text(screen, "Space - Shoot", 28, WIDTH//2, HEIGHT//2 + 45, WHITE)
            draw_text(screen, "X - Shield (if owned)", 28, WIDTH//2, HEIGHT//2 + 70, WHITE)
            draw_text(screen, "P - Pause", 28, WIDTH//2, HEIGHT//2 + 95, WHITE)

            draw_text(screen, f"High Score: {high_score}", 28, WIDTH//2, HEIGHT//2 + 115, YELLOW)
            draw_text(screen, f"Coins: {coins}", 28, WIDTH//2, HEIGHT//2 + 140, YELLOW)

            draw_text(screen, "Press ENTER to Start", 42, WIDTH//2, HEIGHT//2 + 175, GREEN)
            draw_text(screen, "Press S for Shop", 28, WIDTH//2, HEIGHT//2 + 210, BLUE)
            draw_text(screen, "Press H for Ship Select", 28, WIDTH//2, HEIGHT//2 + 235, (255, 165, 0))
            draw_text(screen, "Press O for Sound Settings", 28, WIDTH//2, HEIGHT//2 + 260, (255, 100, 255))
            draw_text(screen, "Press N for New Game", 28, WIDTH//2, HEIGHT//2 + 285, RED)

        elif game_state == GameState.SHOP:
            draw_text(screen, "SHOP", 72, WIDTH//2, 80, WHITE)
            draw_text(screen, f"Coins: {coins}", 36, WIDTH//2, 130, YELLOW)

            items = [
                ("MULTI SHOT LV1", 300, multi_shot_level >= 1),
                ("MULTI SHOT LV2", 800, multi_shot_level >= 2),
                ("SHIELD", 500, shield_level >= 1),
                ("RAPID FIRE", 350, rapid_fire_level >= 1)
            ]

            for i, (item_name, price, owned) in enumerate(items):
                y_pos = 170 + i * 35
                color = WHITE

                if i == shop_selection:
                    color = GREEN
                    pygame.draw.rect(screen, (0, 50, 0), (WIDTH//2 - 180, y_pos - 15, 360, 30), 2)

                if owned:
                    draw_text(screen, f"{item_name} - OWNED", 24, WIDTH//2, y_pos, color)
                else:
                    can_afford = coins >= price
                    draw_text(screen, f"{item_name} - {price} coins", 24, WIDTH//2, y_pos, color)

            draw_text(screen, "Use UP/DOWN arrows to select", 24, WIDTH//2, HEIGHT - 80, WHITE)
            draw_text(screen, "ENTER to buy, ESC to return", 24, WIDTH//2, HEIGHT - 50, WHITE)

        elif game_state == GameState.SHIP_SELECT:
            draw_text(screen, "SHIP HANGAR", 72, WIDTH//2, 80, WHITE)
            draw_text(screen, f"Coins: {coins}", 36, WIDTH//2, 130, YELLOW)

            draw_text(screen, "OWNED SHIPS:", 36, WIDTH//2, 170, GREEN)

            for i, ship_name in enumerate(owned_ships):
                y_pos = 210 + i * 40
                color = WHITE
                ship_display_name = ship_name.upper().replace('_', ' ')

                if i == ship_selection:
                    color = GREEN
                    pygame.draw.rect(screen, (0, 50, 0), (WIDTH//2 - 150, y_pos - 15, 300, 30), 2)

                if ship_name == ship_skin:
                    draw_text(screen, f"{ship_display_name} - ACTIVE", 28, WIDTH//2, y_pos, color)
                else:
                    draw_text(screen, ship_display_name, 28, WIDTH//2, y_pos, color)

            available_ships = ['astro', 'fighter', 'stealth', 'classic']
            prices = [500, 750, 600, 400]
            unowned_ships = [(ship, price) for ship, price in zip(available_ships, prices) if ship not in owned_ships]

            if unowned_ships:
                draw_text(screen, "AVAILABLE FOR PURCHASE:", 32, WIDTH//2, 350, BLUE)
                for i, (ship_name, price) in enumerate(unowned_ships):
                    y_pos = 380 + i * 30
                    ship_display_name = ship_name.upper().replace('_', ' ')
                    can_afford = coins >= price
                    color = GREEN if can_afford else RED
                    draw_text(screen, f"{ship_display_name} - {price} coins", 24, WIDTH//2, y_pos, color)

            draw_text(screen, "UP/DOWN to select, ENTER to equip", 20, WIDTH//2, HEIGHT - 80, WHITE)
            draw_text(screen, "B to buy next affordable ship", 20, WIDTH//2, HEIGHT - 60, WHITE)
            draw_text(screen, "ESC to return to menu", 20, WIDTH//2, HEIGHT - 40, WHITE)

        elif game_state == GameState.SOUND_SETTINGS:
            draw_text(screen, "SOUND SETTINGS", 72, WIDTH//2, 80, WHITE)

            settings_options = [
                f"Music Volume: {int(sound_manager.music_volume * 100)}%",
                f"SFX Volume: {int(sound_manager.sfx_volume * 100)}%",
                f"Background Music: {'ON' if sound_manager.music_enabled else 'OFF'}",
                f"Sound Effects: {'ON' if sound_manager.sfx_enabled else 'OFF'}"
            ]

            for i, option in enumerate(settings_options):
                y_pos = 150 + i * 40
                color = WHITE

                if i == sound_selection:
                    color = GREEN
                    pygame.draw.rect(screen, (0, 50, 0), (WIDTH//2 - 200, y_pos - 15, 400, 30), 2)

                draw_text(screen, option, 28, WIDTH//2, y_pos, color)

            draw_text(screen, "Use UP/DOWN to select", 24, WIDTH//2, HEIGHT - 120, WHITE)
            draw_text(screen, "Use LEFT/RIGHT to adjust", 24, WIDTH//2, HEIGHT - 90, WHITE)
            draw_text(screen, "ESC to return to menu", 24, WIDTH//2, HEIGHT - 60, WHITE)

        elif game_state == GameState.NEW_GAME_CONFIRM:
            # Semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            # Confirmation dialog box
            dialog_width = 500
            dialog_height = 200
            dialog_x = WIDTH // 2 - dialog_width // 2
            dialog_y = HEIGHT // 2 - dialog_height // 2

            pygame.draw.rect(screen, (40, 40, 40), (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), 3)

            draw_text(screen, "NEW GAME", 48, WIDTH//2, dialog_y + 40, RED)
            draw_text(screen, "This will reset ALL progress except high score!", 24, WIDTH//2, dialog_y + 80, YELLOW)
            draw_text(screen, "You will lose all coins, ships, and upgrades!", 24, WIDTH//2, dialog_y + 105, YELLOW)

            draw_text(screen, "Are you sure?", 32, WIDTH//2, dialog_y + 140, WHITE)
            draw_text(screen, "Press Y to confirm, N to cancel", 28, WIDTH//2, dialog_y + 170, GREEN)

        elif game_state == GameState.GAME_OVER:
            draw_text(screen, "GAME OVER", 72, WIDTH//2, HEIGHT//2 - 50, RED)
            draw_text(screen, f"Final Score: {score}", 48, WIDTH//2, HEIGHT//2, WHITE)
            draw_text(screen, f"High Score: {high_score}", 36, WIDTH//2, HEIGHT//2 + 40, YELLOW)
            draw_text(screen, "Press R to restart", 36, WIDTH//2, HEIGHT//2 + 80, GREEN)
            draw_text(screen, "Press M for menu", 36, WIDTH//2, HEIGHT//2 + 115, BLUE)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()