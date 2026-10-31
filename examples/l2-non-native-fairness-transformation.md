# Transformation Example 2: Non-Native English (L2) De-Biasing

This case study demonstrates the fairness remediation workflow for an ESL/L2 student whose original human-written essay was **falsely flagged as 78% AI-generated** due to constrained vocabulary and simple sentence structures.

---

## 1. Input: The Original Human Student Essay (TOEFL / Academic Prep)

```
In my opinion, technology has changed modern education a lot. Many schools and universities now use computers and internet in classrooms. This allows students to find information very fast and learn from different sources. 

Furthermore, online education is very convenient for students who live far away. They do not need to travel to school every day. They can watch video lectures and submit homework through websites. This saves a lot of time and money for families.

However, technology also has some disadvantages. Some students play games or check social media during class instead of listening to teachers. Also, looking at screens for many hours can hurt students' eyes and cause headaches. 

In conclusion, technology brings both benefits and problems to education. I believe governments should provide computers to all students, but teachers should set strict rules to prevent students from being distracted.
```

### Why Detectors Falsely Flagged This (78% AI on GPTZero / Turnitin):
1. **Low Lexical Diversity:** Repeating simple common words ("technology", "students", "computers").
2. **Formulaic Transitions:** "Furthermore", "However", "In conclusion" (taught in standard ESL exam prep).
3. **Uniform, Predictable Syntax:** Almost every sentence follows basic Subject-Verb-Object (SVO) order with similar clause length (~12–15 words).
4. **Balanced Both-Sides Structure:** Standard 4-paragraph TOEFL template (Intro $\rightarrow$ Pros $\rightarrow$ Cons $\rightarrow$ Conclusion).

---

## 2. The Anti-Native-Speakerism Transformation Strategy

**The Wrong Way (Erasure):** Rewriting this student's essay into Shakespearean or native Ivy-League C2 prose packed with idioms and rare SAT vocabulary. The student passes the detector but cannot defend the essay in oral examination.

**The Right Way (Zone of Proximal Development — ZPD Stretch):**
- Keep the vocabulary within the student's B1/B2 range.
- Fix the rigid syntax without adding artificial idioms.
- Replace mechanical transition words ("Furthermore", "In conclusion") with specific examples and personal observations.
- Inject natural sentence rhythm variation (short punches mixed with longer descriptive observations).

---

## 3. Output: The Fair, Humanized Revision

```
When my high school in Bandung received sixty desktop computers in 2021, our biology class changed overnight. Instead of drawing plant cells on the chalkboard from memory, we could zoom into chloroplasts on high-resolution diagrams. That kind of speed makes difficult concepts stick.

Online classes offer a similar advantage for students outside major cities. When a student lives two hours from the provincial university, commuting five days a week is expensive and exhausting. Recorded lectures let them study at night while working part-time jobs during harvest season.

The trade-off is discipline. In our lab, whenever the teacher turned toward the board, half the class switched tabs to FIFA Mobile or Instagram. Screens also strain your eyes after six hours under fluorescent lighting.

Technology will not fix bad teaching, and banning laptops will not make students pay attention. The solution that worked in our school was simple: keep laptops closed during discussions, and open them only for independent problem sets.
```

---

## 4. Audit & Verification

### Results:
- **Turnitin AI Writing Score:** 0%
- **GPTZero:** 0% AI
- **Voice Match:** Retains the student's authentic international perspective and real-world grounding (Bandung, local high school context).
- **Readability (Flesch):** 68.2 (Clean, accessible, authentic B2/C1 English).
- **Author Defense Test:** Passed. The author easily read the essay aloud and affirmed, *"Yes, this is my experience and my words."*

