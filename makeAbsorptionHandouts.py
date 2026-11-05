#!/usr/bin/env python3
'''
--------------------------------------------------------------------------------
Author: Jesse A. Rogerson, York University, jesserogerson.com, rogerson@yorku.ca

DESCRIPTION:
----------
Companion to starSpectrumCreator.py. Makes the "Absorption patterns" handouts
that students use to identify the elements in their star's spectrum.

Each handout is one page with five panels, one element per panel, showing that
element's absorption pattern on a flat spectrum over the same wavelength range
as Figure 2 (390-710 nm).

The line positions, depths, and widths are IMPORTED from starSpectrumCreator.py
(LineListDict, line_sigma, makeWavelengths, applyAbsorption), so the handouts
always match the students' spectra exactly. If you change an element there,
just re-run this script.

USAGE:
----------
$> python3 makeAbsorptionHandouts.py

Makes two PDFs, splitting the elements in the order they appear in
LineListDict (first five, last five):
    absorption-patterns-1.pdf   (e.g. Hydrogen, Helium, Lithium, Sodium, Calcium)
    absorption-patterns-2.pdf   (e.g. Magnesium, Nitrogen, Carbon, Oxygen, Iron)

Optional:
  -prefix PREFIX     start of the output filenames
                     (default: absorption-patterns)
  -per_page N        elements per handout (default: 5)

starSpectrumCreator.py must be in the same folder as this script.

HISTORY
--------------------------------------------------------------------------------
2026-11-05 - JAR - created (replaces the original, lost handout script)
--------------------------------------------------------------------------------
'''
import argparse
import numpy as np
import matplotlib.pyplot as plt

from starSpectrumCreator import LineListDict, makeWavelengths, applyAbsorption

def makeHandout(elements, filename):
    '''
    One page (8 x 10 in), one panel per element, stacked vertically.
    '''
    wavelengths = makeWavelengths()
    flat = np.ones_like(wavelengths)  # a perfectly flat spectrum of intensity 1

    fig, axes = plt.subplots(len(elements), 1, figsize=(8, 10))
    axes = np.atleast_1d(axes)

    for ax, element in zip(axes, elements):
        ax.plot(wavelengths, applyAbsorption(wavelengths, flat, [element]),
                color='black')
        ax.set_title('Absorption pattern for {}'.format(element))
        ax.set_ylabel('Intensity')
        ax.set_xlim([390, 710])          # same range as Figure 2
        ax.set_ylim([0, 1.05])           # same scale for every element, so
                                         # line depths can be compared
        ax.set_xticks(np.arange(400, 701, 20))
        ax.grid(True)

    axes[-1].set_xlabel('Wavelength (nm)')
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    print('wrote {}: {}'.format(filename, ', '.join(elements)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-prefix', type=str, default='absorption-patterns',
                        help='start of the output filenames (default: absorption-patterns)')
    parser.add_argument('-per_page', type=int, default=5,
                        help='elements per handout (default: 5)')
    args = parser.parse_args()

    elements = list(LineListDict.keys())
    n = args.per_page
    for i in range(0, len(elements), n):
        makeHandout(elements[i:i+n], '{}-{}.pdf'.format(args.prefix, i//n + 1))
