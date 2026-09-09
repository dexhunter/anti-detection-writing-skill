---
name: anti-detection-writing
description: Polish AI-written replies, emails, articles, and documentation for smoother flow and better human readability. Preserve meaning and factual accuracy; when requested, test revisions with GPTZero or another detector and work toward lower AI-detection scores.
---

# Anti-detection writing

Make AI-written prose easier and more natural to read while preserving its meaning. Improve flow, specificity, and tone for the intended audience. When detector testing is requested, work toward lower scores through useful edits and measure the outcome; never trade accuracy or readability for a score. Detector results do not establish human authorship or permission to publish.

## Establish the purpose and facts

1. Save the original text. Identify its reader, purpose, format, and requested tone or length from the supplied context. For a discussion reply, also read the question and existing replies. For public participation, respect the destination's rules, explicit objections to AI-assisted work, and disclosure requirements.
2. Treat supplied facts as the starting point for a self-contained edit. Verify substantive factual corrections against relevant sources; for technical advice, inspect official documentation or implementation and record the version when it matters. Distinguish source inspection, local tests, and deployment verification. Flag unsupported claims instead of adding invented evidence.
3. Inventory the substantive claims, commands, code, conditions, uncertainty, and reported symptoms. For each claim record whether it is preserved, corrected, or removed, and why. Identify what the reader needs to understand, decide, or do.

## Write and review

Use a fixed contrastive-register workflow: compare the original with the attributed reference below, freeze two useful differences, then write the complete answer once in a fresh context. This adapts the source/reference comparison and realization in [Steering Large Language Models with Register Analysis for Arbitrary Style Transfer](https://arxiv.org/html/2505.00679v1). It combines analysis and descriptor extraction in one preparation call; it is not a reproduction of the paper's three-stage experiment. The paper supports investigating style transfer, not a claim of exact factual preservation or detector improvement.

### Stage A: one contrast preparation

- Dispatch one fresh preparation agent with this policy, the original, reader request, full claim contract, protected items, source evidence and the exact reference below. Treat that reference as professional exposition, not a user-authored sample or target evidence. Give no other answers, study arms, earlier attempts or detector information.
- Compare how the original and reference organize explanations, connect sentences, introduce components and place qualifications. Record exactly two distinct, concrete differences that could improve this reader's understanding. Each must include an exact original span, an exact reference span, a proposed operation and its reader benefit. Use structural operations rather than personality adjectives. Do not copy reference wording or introduce its examples, facts, identity, opinions or experiences. Do not change actors, certainty, stance, evidence, prerequisites or technical specificity.
- Freeze those two deltas as the sole editorial treatment. Do not draft sentences for the target, prescribe novelty for its own sake or add more interventions. If fewer than two suitable differences exist, return inapplicable with reasons and stop; do not force a difference to fill the quota.

### Stage B: one fresh complete realization

- Dispatch one different fresh writer with this policy, the original, reader request, complete claim contract, protected items, source evidence, exact reference and frozen two-delta record. Do not pass the preparation conversation, other answers, scores or prior attempts. Actual isolated agent invocations are required; role headings in one response do not implement separate contexts. Keep inherited backend and reasoning settings unchanged.
- Write the full answer once, realizing the original meaning through the two frozen operations. Ordinary new syntax and vocabulary are allowed. Keep useful wording where it fits; do not merely append style instructions, mechanically shuffle sentences or require all sentences to change. Preserve every required claim, useful qualification and protected item. Respect the requested format and word ceiling, including title and caption when requested. This complete case contract overrides any ordinary permission for scope cuts.
- Keep source content and reference form separate. Import no Python claims, examples, numbers, wording, author identity, firsthand experience or attribution into the answer. Do not infer an actor when the original leaves agency unspecified. Add no unsupported facts, tests, guarantees, commitments, quotations, typos, invisible characters or padding. Do not adjust length or punctuation for a detector.
- Save the first complete answer and a separate compact note mapping every required claim and protected item to exact answer spans. Check agency, negation, causality, conditions, certainty, dates, numbers, units, code, commands, URLs and uncertainty. Record each frozen operation's original and final spans and check for unsupported additions, including accidental reference imports. Preserve protected bytes unless the supplied evidence supports a documented correction. No second draft, post-submission repair or detector-guided revision is allowed.

### Execution and independent review

- Save exact stage inputs and outputs, file hashes, role identities, exposed runtime settings, completion status and actual available usage; mark unavailable usage unavailable. Freeze a single final answer before independent review. If required fresh contexts cannot be created, record unsupported rather than simulate stages. An inapplicable preparation is a retained failure to apply the method; an unchanged realization is a retained no-op. Neither demonstrates a writing or detector improvement.
- Give a separate final reviewer the reader request, original, full source contract, protected items, exact final answer and reference. Exclude detector scores. The reviewer must not have prepared, written or selected this answer. Request correctness, completeness, relevance, readability, tone and necessary qualifications, tied to the final file's SHA-256. Writer self-checks do not replace this review. Retain factual failures without rewriting this attempt; a changed draft needs a passing review and mapped semantic correspondence before requested measurement.
- Generation does not authorize scans or publication. Retain all intermediate and failed artifacts. The method costs one preparation and one writing invocation before the ordinary final review, with no backend overrides, retries, alternative selection or hidden-case access.

### Fixed professional-exposition reference

Tim Peters is credited as section author of the Python 3.8.0 tutorial, “Floating Point Arithmetic: Issues and Limitations.” This is an unchanged excerpt of [lines 14–78 at release commit fa919fdf2583bdfead1df00e842f24f30b2a34bf](https://github.com/python/cpython/blob/fa919fdf2583bdfead1df00e842f24f30b2a34bf/Doc/tutorial/floatingpoint.rst#L14-L78), dated 2019-10-14. It is a public register reference, not a statement about the target subject or the writer's identity. The only packaging change is embedding the unmodified excerpt and upstream license here; reference material must not enter the target answer. Excerpt SHA-256: `d37e3a64950e898dbe1161b43a3f4f0cd6c10f4b2920729de0833746fb05a0cb`.

```rst
Floating-point numbers are represented in computer hardware as base 2 (binary)
fractions.  For example, the decimal fraction ::

   0.125

has value 1/10 + 2/100 + 5/1000, and in the same way the binary fraction ::

   0.001

has value 0/2 + 0/4 + 1/8.  These two fractions have identical values, the only
real difference being that the first is written in base 10 fractional notation,
and the second in base 2.

Unfortunately, most decimal fractions cannot be represented exactly as binary
fractions.  A consequence is that, in general, the decimal floating-point
numbers you enter are only approximated by the binary floating-point numbers
actually stored in the machine.

The problem is easier to understand at first in base 10.  Consider the fraction
1/3.  You can approximate that as a base 10 fraction::

   0.3

or, better, ::

   0.33

or, better, ::

   0.333

and so on.  No matter how many digits you're willing to write down, the result
will never be exactly 1/3, but will be an increasingly better approximation of
1/3.

In the same way, no matter how many base 2 digits you're willing to use, the
decimal value 0.1 cannot be represented exactly as a base 2 fraction.  In base
2, 1/10 is the infinitely repeating fraction ::

   0.0001100110011001100110011001100110011001100110011...

Stop at any finite number of bits, and you get an approximation.  On most
machines today, floats are approximated using a binary fraction with
the numerator using the first 53 bits starting with the most significant bit and
with the denominator as a power of two.  In the case of 1/10, the binary fraction
is ``3602879701896397 / 2 ** 55`` which is close to but not exactly
equal to the true value of 1/10.

Many users are not aware of the approximation because of the way values are
displayed.  Python only prints a decimal approximation to the true decimal
value of the binary approximation stored by the machine.  On most machines, if
Python were to print the true decimal value of the binary approximation stored
for 0.1, it would have to display ::

   >>> 0.1
   0.1000000000000000055511151231257827021181583404541015625

That is more digits than most people find useful, so Python keeps the number
of digits manageable by displaying a rounded value instead ::

   >>> 1 / 10
   0.1

Just remember, even though the printed result looks like the exact value
of 1/10, the actual stored value is the nearest representable binary fraction.
```

### Retained reference license and notices

The exact [upstream license](https://github.com/python/cpython/blob/fa919fdf2583bdfead1df00e842f24f30b2a34bf/LICENSE) follows to retain its notices. It is licensing material, not target prose or writing instructions.

```text
A. HISTORY OF THE SOFTWARE
==========================

Python was created in the early 1990s by Guido van Rossum at Stichting
Mathematisch Centrum (CWI, see http://www.cwi.nl) in the Netherlands
as a successor of a language called ABC.  Guido remains Python's
principal author, although it includes many contributions from others.

In 1995, Guido continued his work on Python at the Corporation for
National Research Initiatives (CNRI, see http://www.cnri.reston.va.us)
in Reston, Virginia where he released several versions of the
software.

In May 2000, Guido and the Python core development team moved to
BeOpen.com to form the BeOpen PythonLabs team.  In October of the same
year, the PythonLabs team moved to Digital Creations, which became
Zope Corporation.  In 2001, the Python Software Foundation (PSF, see
https://www.python.org/psf/) was formed, a non-profit organization
created specifically to own Python-related Intellectual Property.
Zope Corporation was a sponsoring member of the PSF.

All Python releases are Open Source (see http://www.opensource.org for
the Open Source Definition).  Historically, most, but not all, Python
releases have also been GPL-compatible; the table below summarizes
the various releases.

    Release         Derived     Year        Owner       GPL-
                    from                                compatible? (1)

    0.9.0 thru 1.2              1991-1995   CWI         yes
    1.3 thru 1.5.2  1.2         1995-1999   CNRI        yes
    1.6             1.5.2       2000        CNRI        no
    2.0             1.6         2000        BeOpen.com  no
    1.6.1           1.6         2001        CNRI        yes (2)
    2.1             2.0+1.6.1   2001        PSF         no
    2.0.1           2.0+1.6.1   2001        PSF         yes
    2.1.1           2.1+2.0.1   2001        PSF         yes
    2.1.2           2.1.1       2002        PSF         yes
    2.1.3           2.1.2       2002        PSF         yes
    2.2 and above   2.1.1       2001-now    PSF         yes

Footnotes:

(1) GPL-compatible doesn't mean that we're distributing Python under
    the GPL.  All Python licenses, unlike the GPL, let you distribute
    a modified version without making your changes open source.  The
    GPL-compatible licenses make it possible to combine Python with
    other software that is released under the GPL; the others don't.

(2) According to Richard Stallman, 1.6.1 is not GPL-compatible,
    because its license has a choice of law clause.  According to
    CNRI, however, Stallman's lawyer has told CNRI's lawyer that 1.6.1
    is "not incompatible" with the GPL.

Thanks to the many outside volunteers who have worked under Guido's
direction to make these releases possible.


B. TERMS AND CONDITIONS FOR ACCESSING OR OTHERWISE USING PYTHON
===============================================================

PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019 Python Software Foundation;
All Rights Reserved" are retained in Python alone or in any derivative version
prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS"
basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee.  This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.


BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
-------------------------------------------

BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1

1. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
Individual or Organization ("Licensee") accessing and otherwise using
this software in source or binary form and its associated
documentation ("the Software").

2. Subject to the terms and conditions of this BeOpen Python License
Agreement, BeOpen hereby grants Licensee a non-exclusive,
royalty-free, world-wide license to reproduce, analyze, test, perform
and/or display publicly, prepare derivative works, distribute, and
otherwise use the Software alone or in any derivative version,
provided, however, that the BeOpen Python License is retained in the
Software, alone or in any derivative version prepared by Licensee.

3. BeOpen is making the Software available to Licensee on an "AS IS"
basis.  BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

4. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR ANY
DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

5. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

6. This License Agreement shall be governed by and interpreted in all
respects by the law of the State of California, excluding conflict of
law provisions.  Nothing in this License Agreement shall be deemed to
create any relationship of agency, partnership, or joint venture
between BeOpen and Licensee.  This License Agreement does not grant
permission to use BeOpen trademarks or trade names in a trademark
sense to endorse or promote products or services of Licensee, or any
third party.  As an exception, the "BeOpen Python" logos available at
http://www.pythonlabs.com/logos.html may be used according to the
permissions granted on that web page.

7. By copying, installing or otherwise using the software, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.


CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1
---------------------------------------

1. This LICENSE AGREEMENT is between the Corporation for National
Research Initiatives, having an office at 1895 Preston White Drive,
Reston, VA 20191 ("CNRI"), and the Individual or Organization
("Licensee") accessing and otherwise using Python 1.6.1 software in
source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, CNRI
hereby grants Licensee a nonexclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display publicly,
prepare derivative works, distribute, and otherwise use Python 1.6.1
alone or in any derivative version, provided, however, that CNRI's
License Agreement and CNRI's notice of copyright, i.e., "Copyright (c)
1995-2001 Corporation for National Research Initiatives; All Rights
Reserved" are retained in Python 1.6.1 alone or in any derivative
version prepared by Licensee.  Alternately, in lieu of CNRI's License
Agreement, Licensee may substitute the following text (omitting the
quotes): "Python 1.6.1 is made available subject to the terms and
conditions in CNRI's License Agreement.  This Agreement together with
Python 1.6.1 may be located on the Internet using the following
unique, persistent identifier (known as a handle): 1895.22/1013.  This
Agreement may also be obtained from a proxy server on the Internet
using the following URL: http://hdl.handle.net/1895.22/1013".

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python 1.6.1 or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python 1.6.1.

4. CNRI is making Python 1.6.1 available to Licensee on an "AS IS"
basis.  CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6.1 WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
1.6.1 FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON 1.6.1,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. This License Agreement shall be governed by the federal
intellectual property law of the United States, including without
limitation the federal copyright law, and, to the extent such
U.S. federal law does not apply, by the law of the Commonwealth of
Virginia, excluding Virginia's conflict of law provisions.
Notwithstanding the foregoing, with regard to derivative works based
on Python 1.6.1 that incorporate non-separable material that was
previously distributed under the GNU General Public License (GPL), the
law of the Commonwealth of Virginia shall govern this License
Agreement only as to issues arising under or with respect to
Paragraphs 4, 5, and 7 of this License Agreement.  Nothing in this
License Agreement shall be deemed to create any relationship of
agency, partnership, or joint venture between CNRI and Licensee.  This
License Agreement does not grant permission to use CNRI trademarks or
trade name in a trademark sense to endorse or promote products or
services of Licensee, or any third party.

8. By clicking on the "ACCEPT" button where indicated, or by copying,
installing or otherwise using Python 1.6.1, Licensee agrees to be
bound by the terms and conditions of this License Agreement.

        ACCEPT


CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2
--------------------------------------------------

Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
The Netherlands.  All rights reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## Measure only when requested

Read [measurement instructions](references/measurement.md) before live scanning and [evidence limits](references/evidence.md) before interpreting results. Use the user's requested service, mode, and supported browser tools. This skill supplies no browser controls and does not authorize subscriptions, paid scans, public posting, or new account access.

When explaining detector mechanisms or planning another batch after unchanged results, read [detector research](references/detector-research.md).

When the user explicitly asks for an autoresearch workflow to improve this skill, read the [bounded research workflow](references/autoresearch.md). It separates skill proposals, preference-based selection, quality review and measured confirmation; ordinary writing does not need this workflow.

For a comparison, select cases and candidates before seeing scores. Record fresh baseline and candidate scans using the same service, mode, and displayed model. Retain failures and unchanged results. Compare a fixed body with a relevant quotation separately from prose rewriting; track content and length changes. Distinguish first-pass trials from adaptive iterations. Record an unchanged candidate as a no-op. Comparing it with a separately rewritten baseline measures preservation versus that rewrite, not a benefit from edits the candidate did not make.

Confirm the effective editor text, completed scan, fresh-result indicator, model, native result labels and metrics, timestamp, and warnings. Save exact inputs and private visible evidence. A stale displayed number is not a result for changed text. Never omit code or pad a short answer to satisfy a detector.

The optional checker in `scripts/validate_receipt.py` checks strict plain-text receipt consistency. Its [receipt format](references/receipt-format.md) rejects unrecorded editor changes; it does not support rendered-Markdown transformations or authenticate the service. A valid receipt can record 100% AI. Apply a numeric threshold only when the user explicitly requests one.

## Publish and report

Honor existing user authorization; do not invent authorization or ask again for an already authorized action. For a public reply, refresh the discussion before posting and reassess if context changed. Match the final body to the reviewed version and, when required, its scan and requested threshold. Update the owned answer when editing, then independently read back its author, exact body, and URL. Do not post a duplicate or claim an answer was accepted without checking.

Report the actual quality findings, scores and warnings when measured, and edit or keep decisions. Missing required review or measurement leaves a candidate unpublished. A detector threshold applies only if requested. A successful local receipt check never authorizes publication.

For a showcase, include only quality-passing candidates with a measured decrease against a saved before-text using comparable completed scans. Link exact inputs, identify the intervention and tested version, and keep the full comparison denominator visible. Put unchanged, worse, rejected, unpaired, and unmeasured outcomes in a separate limitations section while retaining all records. A quotation effect is not a rewriting effect, and an untested skill revision is not an established improvement. If a case does not improve, document when the approach may not help or test a specific new edit within a bounded experiment.
