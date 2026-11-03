# Jayati Rai portfolio (rebuild)

Static site: `index.html`, `styles.css`, `script.js`. No build step. It follows the system light or dark theme.

## Before publishing

1. `resume.pdf` is already included and the site buttons download it as `Jayati_Rai_Resume.pdf`. It is built from `resume/build_resume.py`: edit the CONTENT block, run `pip install reportlab`, then `python build_resume.py resume.pdf` and copy the result into `portfolio/`. Before sending it, check the city, add a phone number if you want one, and add any experience or achievements.
2. The project images are already in `images/` as compressed WebP (about 230 KB in total, down from about 3.9 MB). Replace them with newer screenshots if you have them.
3. Make the case studies specific: your role, users, results, Play Store or demo links. Every "Problem / What I built / Result" line is written from the old site's descriptions.
4. Check the wording written for you: the "How I got here" paragraphs, the "Right now" list, and the "Used in" lines under Skills (for example, Ktor and REST APIs are marked as coursework).
5. Add CGPA or percentages to the timeline if they help.

## Publish on GitHub Pages

Replace the contents of the `my_portfolio` repository with the files in `portfolio/` and push.

## Performance note

Lighthouse scores 100 for accessibility, best practices and SEO. Images are local WebP files sized for the cards, so the page is light.
