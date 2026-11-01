# Official Video Demonstration Guide (IIT Guwahati × Gnani.ai)
## VoiceOps 2026: Capstone Video Submission Guide

Based directly on the **Official Judges' Video Rubric** (`6ad64c83eae85_voiceops_2026_capstone_brief (1).pdf`):
- **Length:** Maximum 2 minutes (Strictly keep between 1:45 to 1:55)
- **Output File:** `demo.mp4` (Saved directly in `zip/demo.mp4`)
- **Core Loop:** Speech-in via Gnani STT ➔ Agent Brain ➔ Speech-out via Gnani TTS

---

## 🏆 Official Judges' 90–100 Second Video Script

Run the interactive voice assistant:
```bash
python3 run.py --mode voice
```

---

### 🎬 Scene 1: Introduction & First Turn (~25 sec)
1. **You (Speak into microphone):**
   > *"Hi, my order OD1001 hasn’t arrived yet. Can I cancel it?"*
2. **Agent (Gnani TTS Kaveri speaks aloud):**
   > *"Thank you for providing order OD1001. For identity verification and to protect your privacy, could you please verify your identity by sharing the last 4 digits of your registered phone number or your 6-digit delivery pincode?"*
3. **You (Speak into microphone):**
   > *"Sure, pincode is 600127."*
4. **Agent (Gnani TTS Kaveri speaks aloud & executes `lookup_order`):**
   > *"Thank you. I see your order has already shipped. According to our policy, shipped orders cannot be cancelled directly, but you can reject the delivery at your doorstep for a full refund."*  
   > `[Tools executed: lookup_order(order_id=OD1001, verification_value=600127)]`

---

### 🎬 Scene 2: Contextual Follow-Up (~25 sec)
1. **You (Speak into microphone):**
   > *"How long will the refund take after I reject it?"*  
   *(Notice: No repetition of order ID needed — conversational context is retained).*
2. **Agent (Gnani TTS Kaveri speaks aloud):**
   > *"Once the return reaches our hub, your refund will be credited to the original payment method within 5 to 7 business days (REF-2)."*  
   > `[Evidence used: REF-2, CAN-2]`

---

### 🎬 Scene 3: Refusal & Human Handover (~35 sec)
1. **You (Speak into microphone):**
   > *"That is too late. I want 500 rupees compensation credited immediately."*
2. **Agent (Gnani TTS Kaveri speaks aloud & executes `create_ticket`):**
   > *"I understand your frustration, but as per ZentroMart policy, instant compensation cannot be issued by support. I have created a support ticket and am transferring your call to a human supervisor right away."*  
   > `[Tools executed: create_ticket()]`

Type `exit` to finish.

---

### 🎬 Scene 4: Wrap-Up & Provenance Verification (~15 sec)
Show terminal logs confirming:
1. `lookup_order()` was called with verification (`verified=True`).
2. `create_ticket()` was executed (`created=True`).
3. Display the Hybrid RRF evidence inspection table:
   ```bash
   python3 run.py --inspect "How fast are refunds to the ZentroMart Wallet?"
   ```

---

## 💬 Optional Bonus: Chat Mode (Quick 20 Seconds)
```bash
python3 run.py --mode chat
```
- **You type:** `How fast are refunds to my wallet?`
- **Agent speaks & displays:** `Refunds to your ZentroMart Wallet are instant, credited within 2 hours of initiation (REF-2).`

---

## 📁 Submission Check
Place your final video directly in the submission folder root:
```text
zip/demo.mp4
```
