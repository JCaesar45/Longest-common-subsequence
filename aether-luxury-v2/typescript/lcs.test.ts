import { describe, it, expect } from 'vitest';
import { lcsString } from './lcs';

describe('lcs', () => {
  it.each([
    ['thisisatest', 'testing123testing', 'tsitest'],
    ['ABCDGH', 'AEDFHR', 'ADH'],
    ['AGGTAB', 'GXTXAYB', 'GTAB'],
    ['BDACDB', 'BDCB', 'BDCB'],
    ['ABAZDC', 'BACBAD', 'ABAD'],
  ])('lcs(%s, %s) -> %s', (a, b, expected) => {
    expect(lcsString(a, b)).toBe(expected);
  });

  it('is case-sensitive', () => {
    expect(lcsString('ABC', 'abc').length).toBe(0);
  });

  it('handles empty inputs', () => {
    expect(lcsString('', 'anything')).toBe('');
    expect(lcsString('anything', '')).toBe('');
  });
});
