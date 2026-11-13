# CHAPTER 2 – LITERATURE SURVEY

## 2.1 Overview of Automatic Speech Recognition (ASR)

Automatic Speech Recognition (ASR) has evolved dramatically from early template-matching Dynamic Time Warping (DTW) algorithms and Hidden Markov Models with Gaussian Mixture Models (HMM-GMMs) to deep neural network acoustic models (HMM-DNNs), and ultimately to end-to-end (E2E) sequence-to-sequence deep learning architectures.

### 2.1.1 Evolution of End-to-End ASR Architectures
Early statistical ASR systems decoupled acoustic modeling, pronunciation lexicons, and n-gram language models, requiring intensive manual feature engineering and phonetic alignment. The transition to Connectionist Temporal Classification (CTC) introduced by Graves et al. (2006) enabled direct recurrent neural network (RNN) training on unaligned audio-text pairs. Subsequent developments introduced Listen, Attend and Spell (LAS) by Chan et al. (2016), utilizing attention-based encoder-decoder networks to model speech-to-text conversion holistically.

In recent years, the Conformer architecture (Gulati et al., 2020) combined self-attention with depthwise separable convolutions to capture both global receptive field context and local shift-invariant acoustic features simultaneously. Conformer networks have achieved state-of-the-art performance on standardized benchmarks such as LibriSpeech.

### 2.1.2 OpenAI Whisper Architecture and Weak Supervision
Radford et al. (2022) introduced Whisper, an encoder-decoder Transformer trained on 680,000 hours of weakly supervised multilingual and multitask audio collected from the public web. Whisper processes raw audio resampled to 16 kHz by computing 80-channel log-magnitude Mel-spectrogram representations using 25-millisecond windows with a 10-millisecond stride. The encoder uses two convolutional layers with a stride of 2, followed by sinusoidal positional embeddings and stacked Transformer encoder blocks.

The Whisper decoder is an autoregressive Transformer decoder that predicts a sequence of special tokens and text tokens, interleaving language identification (`<|hi|>`), task specification (`<|transcribe|>` or `<|translate|>`), timestamp prediction, and transcribed text. Whisper's extensive multilingual pretraining demonstrates remarkable zero-shot robustness across varying acoustic environments, background noise profiles, and non-native conversational accents.

### 2.1.3 Speech Recognition in Indian Vernacular Contexts
Speech recognition across Indian languages presents unique acoustic and phonetic hurdles:
- **Phonetic Richness:** Indian languages (both Indo-Aryan and Dravidian) possess extensive phonetic repertoires featuring retroflex consonants (e.g., /ʈ/, /ɖ/), aspirated plosives (e.g., /kʰ/, /ɡʱ/), and nasalized vowels that do not exist in Western languages.
- **Acoustic Diversity & Dialects:** High acoustic variance across sub-regional accents, pitch variations, and rapid conversational speaking rates.
- **Acoustic Noise Environments:** Real-world audio captured on mobile devices across Indian public settings frequently exhibits ambient traffic noise, reverberation, and crowd chatter with low Signal-to-Noise Ratios (SNR < 15 dB).
- **IndicConformer and IndicWav2Vec:** AI4Bharat (Javed et al., 2021; Kumar et al., 2022) developed IndicWav2Vec and IndicConformer, fine-tuning acoustic models across thousands of hours of Indian speech data, establishing competitive baselines for Indian language transcription.

---

## 2.2 Neural Machine Translation (NMT) for Indic Languages

### 2.2.1 From Statistical to Transformer-Based Machine Translation
Machine translation research has progressed through three primary paradigms:
1. **Rule-Based Machine Translation (RBMT):** Relying on bilingual dictionaries and hand-crafted syntactic parse trees, failing completely on idiomatic or colloquial expressions.
2. **Statistical Machine Translation (SMT):** Utilizing phrase-based translation tables and n-gram language models (e.g., Moses toolkit). SMT heavily suffered from word order divergence between Subject-Verb-Object (SVO) languages like English and Subject-Object-Verb (SOV) languages characteristic of Indian tongues.
3. **Neural Machine Translation (NMT):** Bahdanau et al. (2014) introduced the additive attention mechanism in encoder-decoder RNNs (LSTMs/GRUs). Vaswani et al. (2017) revolutionized NLP with the Transformer architecture, replacing recurrent inductive biases with multi-head self-attention mechanisms:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### 2.2.2 Massive Multilingual Pretrained Models: NLLB-200 and IndicTrans2
Scaling multilingual translation models has bridged the gap for low-resource languages through cross-lingual transfer learning:
- **No Language Left Behind (NLLB-200):** Introduced by the NLLB Team / Meta AI (2022), NLLB-200 is an encoder-decoder Transformer trained on over 200 languages with architectural scaling up to 54 billion parameters, along with distilled variants (NLLB-200-Distilled-600M and 1.3B). NLLB utilizes a SentencePiece vocabulary of 256,000 subword units with shared representations that facilitate cross-lingual parameter sharing, substantially improving translation quality on low-resource Indic languages.
- **IndicTrans and IndicTrans2:** Gala et al. (2023) from AI4Bharat engineered IndicTrans2, the first open-source sequence-to-sequence model supporting all 22 scheduled Indian languages plus English (supporting 1,012 language directions). IndicTrans2 addresses script diversity through a canonical Devanagari transliteration scheme during training, ensuring parameter sharing across morphologically related Indic roots.

### 2.2.3 Linguistic Challenges in Indic Language Translation
Indian languages present structural complexities distinct from Germanic or Romance languages:
- **Word-Order Divergence:** English adheres to Subject-Verb-Object (SVO), whereas all 10 scheduled Indian languages follow Subject-Object-Verb (SOV).
- **Morphological Richness and Agglutination:** Dravidian languages (Tamil, Telugu, Kannada, Malayalam) are agglutinative, attaching long chains of grammatical suffixes to verbal and nominal roots. Standard word-level tokenizers suffer from high Out-Of-Vocabulary (OOV) rates, necessitating subword byte-pair or unigram tokenization.
- **Honorifics and Gender-Number-Person (GNP) Agreement:** Indic verbs and adjectives must agree with the gender, number, and formal politeness level of nouns, which are often dropped (pro-drop phenomenon) in conversational speech.

---

## 2.3 Text-to-Speech (TTS) Synthesis Technologies

Speech synthesis transforms normalized text into intelligible, natural acoustic waveforms.

### 2.3.1 Concatenative vs. Parametric vs. Deep Neural TTS
- **Unit Selection & Concatenative TTS:** Recorded speech segments spliced together at synthesis time. Produced robotic transitions, metallic artifacts, and required massive studio voice databases.
- **Deep Neural Two-Stage TTS:** Tacotron 2 (Shen et al., 2018) paired a Seq2Seq recurrent spectrogram predictor with a neural vocoder (e.g., WaveNet or HiFi-GAN) to synthesize speech. While natural, auto-regressive generation was slow and computationally prohibitive for real-time edge devices.
- **Non-Autoregressive TTS (FastSpeech 2):** Ren et al. (2020) introduced feed-forward Transformer blocks with explicit duration, pitch, and energy predictors, enabling rapid parallel generation.

### 2.3.2 VITS and Meta MMS-TTS
Kim et al. (2021) introduced VITS (Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech), a fully end-to-end generative architecture combining:
1. A variational autoencoder (VAE) modeling latent acoustic representations.
2. Normalizing flows to enhance the expressiveness of the prior distribution.
3. Monotonic Alignment Search (MAS) to resolve alignment between phoneme sequences and spectrogram frames without external alignment tools.
4. An adversarial multi-period discriminator (MPD) and multi-scale discriminator (MSD) for direct time-domain waveform synthesis.

Pratap et al. (2023) developed the Massively Multilingual Speech (MMS) project at Meta AI, training VITS models across more than 1,100 languages. MMS-TTS provides lightweight, dedicated single-speaker VITS checkpoints for individual Indian languages (~36M parameters per language checkpoint), offering exceptionally low CPU synthesis latency (~350–500 ms) and high mean opinion scores (MOS > 3.8).

---

## 2.4 Language Identification (LID) and Script Disambiguation

Automated Language Identification serves as the routing nexus in voice translation pipelines:
- **Acoustic LID:** Identifies language directly from spectral audio features (e.g., Whisper's first-token prediction). While effective for distinct phonological families, acoustic LID can falter between closely related languages (e.g., Hindi vs. Marathi or Bengali vs. Assamese).
- **Textual LID (n-gram & Character Profiles):** Cavnar & Trenkle (1994) established n-gram frequency profile classification, implemented in libraries like `langdetect` and `fasttext` (Joulin et al., 2016).
- **Script-Based Deterministic Disambiguation:** Indian languages are written in largely distinct Brahmic-derived scripts:
  - Devanagari: Hindi, Marathi, Sanskrit, Nepali.
  - Bengali-Assamese: Bengali.
  - Gurmukhi: Punjabi.
  - Gujarati: Gujarati.
  - Dravidian scripts: Tamil, Telugu, Kannada, Malayalam.
- **The Devanagari Disambiguation Challenge:** Both Hindi (`hi`) and Marathi (`mr`) share the Devanagari script. Standard Unicode block mapping cannot distinguish them. BhashaAI addresses this through secondary morphological inspection of Marathi-specific postpositions and verb endings (e.g., आहे, नाही, च्या, साठी, करतो).

---

## 2.5 Audio Digital Signal Processing (DSP) & Noise Reduction

Speech recognition models trained on studio data degrade significantly when exposed to non-stationary acoustic noise.
- **Spectral Subtraction:** Boll (1979) introduced spectral subtraction, estimating ambient stationary background noise from non-speech pauses and subtracting noise magnitude spectra from the input signal.
- **Log-Mel Filterbanks and Resampling:** Modern neural ASR architectures require strict 16,000 Hz single-channel (mono) floating-point inputs scaled to $[-1.0, 1.0]$. High-quality sinc interpolation resampling avoids aliasing artifacts.
- **Silence Trimming and Energy Thresholding:** Removing leading and trailing non-speech segments via Root-Mean-Square (RMS) energy thresholding prevents autoregressive hallucination in Transformer decoders.

---

## 2.6 Summary of Related Literature and Benchmark Studies

| Author / Project | Year | Architecture / Core Models | Language Scope | Key Contributions | Limitations / Gaps |
|:---|:---:|:---|:---|:---|:---|
| **Radford et al. (OpenAI)** | 2022 | Whisper (Transformer Encoder-Decoder) | 99+ Languages | Large-scale weakly supervised ASR; robust zero-shot transcription | High compute demands; higher WER on low-resource Indic dialects |
| **Meta AI (NLLB Team)** | 2022 | NLLB-200 (Seq2Seq Transformer) | 200+ Languages | Deep cross-lingual transfer; shared SentencePiece vocabulary | Large parameter counts; memory heavy for edge/CPU inference |
| **Gala et al. (AI4Bharat)** | 2023 | IndicTrans2 (Transformer) | 22 Scheduled Indic + English | Script unification via Devanagari; top Indic translation benchmarks | High VRAM requirements for 1B model; complex deployment dependencies |
| **Pratap et al. (Meta AI)** | 2023 | MMS-TTS (VITS VAE + GAN) | 1,100+ Languages | Ultra-lightweight end-to-end neural speech synthesis | Fixed single-speaker timbre per language; strict phonetic tokenization |
| **Javed et al. (AI4Bharat)** | 2021 | IndicWav2Vec (Self-Supervised) | 22 Indic Languages | Self-supervised acoustic representations for Indian speech | Requires downstream fine-tuning and language-specific CTC decoders |
| **BhashaAI (This Project)** | 2026 | Whisper + NLLB-200 + MMS-TTS + DSP | 10 Scheduled Indic + English | Unified, modular, CPU-optimized voice-to-voice pipeline with empirical evaluation & Web UI | Optimized for 8GB RAM CPU execution; single-speaker synthesis per language |

---

## 2.7 Research Gaps Identified and BhashaAI Value Proposition

1. **Fragmented Implementations:** Existing literature investigates ASR, NMT, and TTS in isolation. Few open-source architectures present a cohesive, modular voice-to-voice system specifically tuned for Indian linguistic constraints.
2. **Neglect of CPU Workstation Environments:** Foundation model research often assumes multi-GPU server clusters. Research into low-latency CPU orchestration on standard 8GB RAM hardware remains scarce.
3. **Over-Reliance on English Pivoting:** Traditional systems pivot through English, compounding translation error. Direct Indic-to-Indic translation pathways must be evaluated natively using BLEU and chrF++.
4. **Lack of Acoustic Preprocessing Integration:** Many ASR pipelines feed raw browser audio directly into neural models, causing hallucination and elevated WER under low SNR conditions.
5. **Absence of Real-Time Latency Telemetry:** Academic publications rarely report end-to-end decomposed pipeline latencies ($T_{\text{DSP}} + T_{\text{ASR}} + T_{\text{LID}} + T_{\text{NMT}} + T_{\text{TTS}}$) under production web-serving constraints.

BhashaAI directly addresses these research gaps by synthesizing robust DSP preprocessing, multilingual deep learning inference, decoupled microservices, and empirical benchmarking into an accessible full-stack application.
