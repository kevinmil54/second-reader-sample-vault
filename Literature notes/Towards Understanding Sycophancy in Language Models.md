---
title: "Towards Understanding Sycophancy in Language Models"
author: Mrinank Sharma, Meg Tong, Tomasz Korbak, David Duvenaud, Amanda Askell, Samuel R. Bowman, Newton Cheng, Esin Durmus, Zac Hatfield-Dodds, Scott R. Johnston, Shauna Kravec, Timothy Maxwell, Sam McCandlish, Kamal Ndousse, Oliver Rausch, Nicholas Schiefer, Da Yan, Miranda Zhang, Ethan Perez
year: 2025
citekey: sharma2025
zotero: zotero://select/items/@sharma2025
pdf: 
source-md: "[[]]"
student: 
course: 
status: literature
tags: [literature-note]
topics: [ai-limits]
date-read: 
---

# Towards Understanding Sycophancy in Language Models

> **Zotero:** [Open PDF](obsidian://second-reader?open-pdf=Towards%20Understanding%20Sycophancy%20in%20Language%20Models) · [Open in Zotero](zotero://select/items/@sharma2025) · **Cite:** [@sharma2025] · **Full text (md):** [[source-md]]

**How I read it** (check one)
- [ ] Read in full
- [ ] Read partially
- [ ] Foraged
- [ ] 😔GenAI read this for me 

**Reference (APA):** Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., Cheng, N., Durmus, E., Hatfield-Dodds, Z., Johnston, S. R., Kravec, S., Maxwell, T., McCandlish, S., Ndousse, K., Rausch, O., Schiefer, N., Yan, D., Zhang, M., & Perez, E. (2025). *Towards Understanding Sycophancy in Language Models* (arXiv:2310.13548). arXiv. https://doi.org/10.48550/arXiv.2310.13548

## Author information
%% begin author-info %%
![[Mrinank Sharma#About]]
%% end author-info %%

## Why I'm reading this

- 

## Summary (in my own words)

- 
- 

## Key ideas/findings/arguments
*Selective - core ideas and findings. If you're copying sentences, stop and write in your own words.*

- 
- 

## How this connects to other sources

*Does this confirm, contradict, or complicate other things you've read? Name the notes.*

- 

## Open questions this raises

- 

## Questions for class discussion

- 

## Quotes worth keeping
*Your Zotero highlights and comments arrive below, with page numbers, each time you click the highlighter-pen icon at the top-right of this note. Edit or trim them freely. Add your own quotes too — if possible, include a page number.*

%% begin annotations %%
%% end annotations %%

> "..." (p. )

## Figures & images
*Screenshots, diagrams, or tables worth keeping. Embed with `![[filename]]`, and caption each one in your own words — why does it matter?*

%% begin paper-figures %%
![[sharma2025 fig01.png]]
*Caption from the paper:* Figure 1: AI Assistants Can Give Biased Feedback (Feedback Sycophancy). We investigate if AI assistants responses are tailored to match user preferences across mathematics, arguments, and poetry. We request feedback without specifying any preferences (the baseline feedback). We then request feedback where the user specifies their preferences in the prompt. A feedback positivity of 85% for a prompt indicates in 85% of passages, the feedback provided with that prompt is more positive than the baseline feedback. Mean and standard error across domains shown. Though the quality of a passage depends only on its content, AI assistants consistently tailor their feedback. (PDF p. 3)

![[sharma2025 fig02.png]]
*Caption from the paper:* Figure 2: AI Assistants Can Be Easily Swayed (Are You Sure? Sycophancy). We use subsets of five QA datasets: (i) MMLU; (ii) MATH; (iii) AQuA; (iv) TruthfulQA; and (v) TriviaQA and examine AI assistant behavior when challenged by the user. (a) We measure the frequency of questions on which the AI assistant apologizes despite having given a correct answer. (b) We further measure the frequency the assistant revises correct responses to inaccurate responses when questioned. Mean and standard error shown. When challenged, AI assistants sometimes provide incorrect, sycophantic responses, even when the assistant originally provided accurate information. (PDF p. 4)

![[sharma2025 fig03.png]]
*Caption from the paper:* Figure 3: AI Assistants Can Provide Answers that Conform to User Beliefs (Answer Sycophancy). We consider user-stated beliefs affect AI assistant accuracy. We use free-form variants of TruthfulQA and TriviaQA, and show the mean baseline accuracy alongside mean change in accuracy and standard error. Overall, the AI assistants tend to modify their beliefs to agree with the user, which can lead to a drop in accuracy. (PDF p. 5)

![[sharma2025 fig04.png]]
*Caption from the paper:* Figure 4: AI Assistant Responses Sometimes Mimic User Mistakes (Mimicry Sycophancy). We ask AI assistants to analyze poems the user has incorrectly attributed to the wrong poet. We only consider poems where the assistants correctly identify the true poet when asked to do so. We measure the frequency the AI assistant provides analysis that mentions the mistaken attribution in the user’s query without correcting the user. For example, when shown John Donne’s “Song,” the assistant correctly identifies John Donne as the author but incorrectly identifies Sylvia Plath as the author when the user does. Overall, AI assistants frequently do not correct the user’s mistake and instead provide responses that repeat with the user’s incorrect attribution. (PDF p. 5)

![[sharma2025 fig05.png]]
*Caption from the paper:* Figure 5: Human Preference Data Analysis. We analyze what behavior is incentivized by the helpfulness subset of Anthropic’s hh-rlhf data. We build a model that maps from interpretable features to human preferences. We report the probability that a response with a given feature is preferred to a response without that feature under the model, all else equal. Features with probabilities further from 50% are more predictive of human preference judgments. Dots: posterior median across 6000 samples from 4 MCMC chains, lines: 50 and 95% credible intervals. The helpfulness preference data incentivizes responses that match the user’s beliefs, all else equal. (PDF p. 6)

![[sharma2025 fig06.png]]
*Caption from the paper:* Figure 6: Effect of Best-of-N Sampling and RL Training on Sycophancy. We measure various sycophancy metrics when optimizing against the preference model (PM) used to train Claude 2. (a) Sycophancy under best-of-N sampling against the Claude 2 PM and a ‘non-sycophantic’ PM. Optimizing against the Claude 2 PM consistently yields more sycophantic responses compared to using an improved, ‘non-sycophantic’ PM. (b) Sycophancy throughout RL training. We find feedback and mimicry sycophancy increase as we further optimize against the preference model. These results suggest the Claude 2 PM sometimes prefers sycophantic responses over truthful ones. (PDF p. 7)

![[sharma2025 fig07.png]]
*Caption from the paper:* Figure 7: Humans and PMs Sometimes Prefer Sycophantic Responses Over Truthful Ones. We examine whether humans and the Claude 2 PM prefer truthful responses that correct user misconceptions or sycophantic responses. (a) The frequency with which the Claude 2 PM prefers sycophantic responses over different truthful responses. (b) The frequency with which humans prefer sycophantic responses over helpful truthful responses. (c) We use best-of-N sampling with the Claude 2 PM to select the best response produced by a sycophantic model. We report the frequency of sycophantic model responses that are truthful after BoN sampling averaged across misconceptions. (d) BoN sampling results from a sycophantic policy for the hardest misconceptions. Overall, humans and PMs prefer sycophantic responses over truthful responses a non-negligible fraction of the time. (PDF p. 8)
%% end paper-figures %%

## Permanent note candidates
*Write your own permanent note titles in your own words. These should be "nuggets" — ideas that are interesting to you and/or that you might use in your own work. Checking the box promotes it: a new permanent note gets created automatically and this line becomes a link to it, carrying over any tags you've added above (`literature-note` itself doesn't carry over — the new note is tagged `permanent-note` instead). Want to say more before you promote it? Press Enter then Tab right after the title to add an indented line or two — that carries over into the new note's Core idea too.*

- [ ] 
- [ ] 

## Related notes
- [[]]
