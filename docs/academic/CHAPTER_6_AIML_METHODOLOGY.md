# CHAPTER 6 – AI/ML METHODOLOGY AND MATHEMATICAL FORMULATION

## 6.1 Deep Learning Architectures

BhashaAI implements three foundational deep neural network architectures to realize its end-to-end voice translation pipeline:

### 6.1.1 Automatic Speech Recognition: OpenAI Whisper
Whisper is formulated as an encoder-decoder Transformer operating directly on audio spectrogram representations.

```mermaid
flowchart LR
    RawAudio["Raw Audio (16kHz)"] --> STFT["STFT & 80-Channel Log-Mel Spectrogram"]
    STFT --> ConvEnc["2x 1D-Convolution (Stride 2)"]
    ConvEnc --> EncTransformer["Transformer Encoder (Stacked Self-Attention)"]
    EncTransformer --> DecTransformer["Transformer Decoder (Cross-Attention)"]
    DecTransformer --> OutputTokens["Autoregressive Text Tokens (BPE)"]
```

1. **Acoustic Front-End:** Audio signals are converted to 80-channel log-magnitude Mel-spectrograms using 25 ms windows with a 10 ms hop size.
2. **Audio Encoder:** Two convolutional layers with filter width 3 and stride 2 downsample the spectrogram temporally by a factor of 4. The downsampled features are added to sinusoidal position embeddings and passed through $N_e$ Transformer encoder blocks with multi-head self-attention.
3. **Autoregressive Decoder:** The decoder utilizes learned positional embeddings and masked multi-head self-attention, followed by cross-attention layers over the encoder hidden states. Special prefix tokens (`<|startoftranscript|>`, `<|hi|>`, `<|transcribe|>`, `<|notimestamps|>`) guide generation.

### 6.1.2 Neural Machine Translation: Meta NLLB-200
NLLB-200 is a sequence-to-sequence Transformer trained across 200+ languages using a shared vocabulary of 256,000 SentencePiece tokens.
- **Encoder:** Encodes tokenized source sequences into continuous contextual representations using standard Transformer encoder blocks.
- **Decoder:** Generates target tokens autoregressively conditioned on source representations and preceding target tokens. A language tag token (e.g., `hin_Deva`, `tam_Taml`) prepended to the decoder prompts target-specific generation.

### 6.1.3 Speech Synthesis: Meta MMS-TTS (VITS)
VITS combines Variational Autoencoders (VAEs), Normalizing Flows, and Generative Adversarial Networks (GANs):
- **Prior Network:** A text encoder transforms phoneme sequences into a prior distribution $\mathcal{N}(\mu(c), \sigma(c))$.
- **Posterior Encoder:** Encodes linear spectrograms of target speech into a latent variable distribution $q(z|x)$.
- **Normalizing Flow:** Improves distribution expressiveness by transforming simple Gaussian priors into complex multi-modal distributions.
- **Monotonic Alignment Search (MAS):** Calculates the optimal monotonic alignment between phoneme lengths and latent frame durations without external phone aligners.
- **HiFi-GAN Decoder:** Generates time-domain waveforms directly from latent variables $z$ using multi-receptive field fusion and multi-period/multi-scale discriminators.

---

## 6.2 Mathematical Formulations

### 6.2.1 Audio Feature Representation: Log-Mel Filterbank
Given a discrete time-domain speech signal $x[n]$, the Short-Time Fourier Transform (STFT) is:

$$X(m, \omega) = \sum_{n=-\infty}^{\infty} x[n] \cdot w[n - m] \cdot e^{-j\omega n}$$

where $w[n]$ represents a Hann window. The power spectrum $|X(m, \omega)|^2$ is filtered through an $M$-channel triangular Mel-filterbank $H_m(k)$:

$$S(m, m') = \sum_{k=0}^{K-1} |X(m, k)|^2 \cdot H_{m'}(k), \quad 1 \le m' \le M$$

The final acoustic feature vector is obtained by computing the logarithm:

$$Y(m, m') = \log\left(\max\left(S(m, m'), 10^{-5}\right)\right)$$

### 6.2.2 Scaled Dot-Product and Multi-Head Attention
Given queries $Q \in \mathbb{R}^{n \times d_k}$, keys $K \in \mathbb{R}^{m \times d_k}$, and values $V \in \mathbb{R}^{m \times d_v}$, attention is calculated as:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

Multi-head attention projects representations into $h$ distinct representation subspaces:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O$$

$$\text{where} \quad \text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$

with parameter projection matrices $W_i^Q \in \mathbb{R}^{d_{\text{model}} \times d_k}$, $W_i^K \in \mathbb{R}^{d_{\text{model}} \times d_k}$, $W_i^V \in \mathbb{R}^{d_{\text{model}} \times d_v}$, and $W^O \in \mathbb{R}^{h d_v \times d_{\text{model}}}$.

### 6.2.3 VITS Objective Formulation
The end-to-end VITS objective optimizes a combination of variational lower bounds and adversarial loss:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{recon}} + \mathcal{L}_{\text{kl}} + \mathcal{L}_{\text{dur}} + \mathcal{L}_{\text{adv}}(G) + \mathcal{L}_{\text{fm}}(G)$$

where:
- $\mathcal{L}_{\text{recon}}$ is the $L_1$ Mel-spectrogram reconstruction loss: $\|x_{\text{mel}} - \hat{x}_{\text{mel}}\|_1$.
- $\mathcal{L}_{\text{kl}}$ is the Kullback-Leibler divergence between posterior latent distribution $q(z|x)$ and text-conditioned prior $p(z|c)$:

$$\mathcal{L}_{\text{kl}} = D_{\text{KL}}(q(z|x) \,\|\, p(z|c))$$

- $\mathcal{L}_{\text{adv}}$ and $\mathcal{L}_{\text{fm}}$ represent the least-squares adversarial discriminator loss and feature matching loss across discriminator intermediate layers.

---

## 6.3 Evaluation Metrics Formulations

### 6.3.1 Word Error Rate (WER) and Character Error Rate (CER)
WER quantifies speech recognition error using the minimum edit (Levenshtein) distance between reference word sequence $R = (r_1, \dots, r_N)$ and hypothesis sequence $H = (h_1, \dots, h_M)$:

$$\text{WER} = \frac{S + D + I}{N}$$

where:
- $S$ = Number of word substitutions.
- $D$ = Number of word deletions.
- $I$ = Number of word insertions.
- $N$ = Total number of words in the ground truth reference.

Character Error Rate (CER) applies the identical Levenshtein edit distance at the individual Unicode character level, providing an essential metric for morphologically rich Indic scripts where minor inflections do not invalidate lexical root recognition.

### 6.3.2 Bilingual Evaluation Understudy (BLEU)
BLEU measures modified n-gram precision between machine translation output and human reference translations:

$$\text{BLEU} = \text{BP} \cdot \exp\left(\sum_{n=1}^N w_n \log p_n\right)$$

where $p_n$ is the modified n-gram precision:

$$p_n = \frac{\sum_{C \in \{\text{Candidates}\}} \sum_{\text{n-gram} \in C} \text{Count}_{\text{clip}}(\text{n-gram})}{\sum_{C' \in \{\text{Candidates}\}} \sum_{\text{n-gram}' \in C'} \text{Count}(\text{n-gram}')}$$

and $\text{BP}$ is the brevity penalty penalizing overly short translations:

$$\text{BP} = \begin{cases} 1 & \text{if } c > r \\ e^{1 - r/c} & \text{if } c \le r \end{cases}$$

Here, $c$ is the candidate hypothesis length and $r$ is the effective reference corpus length. BhashaAI standardizes on 4-gram BLEU with uniform weights $w_n = 1/4$.

### 6.3.3 chrF++ Metric
While BLEU evaluates word n-grams, chrF++ (Popović, 2017) computes F-scores over character n-grams (1 to 6 characters) augmented with word bi-grams:

$$\text{chrF} = (1 + \beta^2) \frac{\text{chrP} \cdot \text{chrR}}{\beta^2 \cdot \text{chrP} + \text{chrR}}$$

where $\text{chrP}$ is character precision, $\text{chrR}$ is character recall, and $\beta=2$ weights recall higher than precision. chrF++ is recognized as vastly more correlated with human judgments for morphologically complex and agglutinative Indian languages.

---

## 6.4 Benchmark Dataset: BhashaAI IN-10 Multi-Parallel Corpus

To rigorously evaluate translation quality across all 10 scheduled languages without bias, we constructed the **BhashaAI IN-10 Multi-Parallel Evaluation Corpus** (`ml/datasets/test_multilingual_corpus.json`).

### 6.4.1 Corpus Composition & Domain Stratification
The benchmark corpus contains parallel sentences across 5 vital conversational and civic domains:
1. **Greetings & Social Interaction:** Everyday conversational phrases.
2. **Governance & Civic Services:** Aadhaar updates, ration cards, administrative requests.
3. **Emergency & Healthcare:** Medical symptoms, hospital queries, emergency directives.
4. **Agriculture & Commerce:** Crop prices, market trading, weather advisories.
5. **Education & Technology:** Digital literacy, school admissions, vocational training.

Each sentence is mutually translated and manually verified across all 10 scheduled languages (Hindi, English, Gujarati, Marathi, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi), yielding a fully dense parallel matrix.

### 6.4.2 Text Normalization Pipeline
Before calculating BLEU and chrF++, both reference and hypothesis strings are routed through a standardized normalization pipeline:
- Unicode NFC normalization.
- Trimming leading/trailing whitespace.
- Removal of zero-width joiners (`\u200d`) and non-breaking spaces.
- Standardized Indic punctuation conversion (e.g., Purna Viram `।` mapped appropriately).
