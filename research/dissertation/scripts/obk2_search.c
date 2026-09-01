/* obk2_search.c — OB-K2 rotation-orbit isotypic construction, exhaustive finite search.
 *
 * Setting (FORMALIZATION.md \S5.5, kill #2): deviation cloud = C_12-orbit of a generic
 * seed w in R^6 under R = block-diag rotations by (2*pi/12)*(1,2,3) on R^2+R^2+R^2.
 * An ordering g of the orbit collides with its rotation-relabel g+1 under H5 iff
 * A1(g) commutes with R. In the eigenbasis of R (eigenvalues w^{s}, s in {+-1,+-2,+-3}):
 *
 *   A1(g)_{pq} = w_p w_q * SUM_{edges a->b} omega^{sig_p * a - sig_q * b}
 *
 * so the collision condition is SEED-INDEPENDENT (any w with all coordinates nonzero):
 *
 *   for all 30 ordered pairs (sig,tau), sig != tau:  SUM_edges omega^{sig*a - tau*b} = 0
 *
 * (the planar reduction Q(g)=SUM omega^{a+b} = 0 is exactly the pair (+1,-1)).
 *
 * Search: exhaustive DFS over orderings g of Z_12 with g[0]=0 fixed (global shift
 * multiplies each condition by a unit; exact vanishing preserved), partial sums kept in
 * exact integer arithmetic in Z[omega] = {c0 + c1*w + c2*w^2 + c3*w^3}, pruned by
 * |S| <= remaining-edge count (unit-circle bound). Admissible pruning only => exhaustive.
 *
 * Modes (argv[1]): "planar" = 1 condition (pair (+1,-1)); "full" = 30 conditions.
 * Prints: nodes explored, witnesses found, first witness permutation (if any).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static const int SIG[6] = {1, -1, 2, -2, 3, -3};
/* add[k] = coefficients of omega^k in basis {1, w, w^2, w^3}, using Phi_12 = x^4 - x^2 + 1 */
static const int ADD[12][4] = {
    {1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1},{-1,0,1,0},{0,-1,0,1},
    {-1,0,0,0},{0,-1,0,0},{0,0,-1,0},{0,0,0,-1},{1,0,-1,0},{0,1,0,-1}};

static int ncond;
static int csig_p[30], csig_q[30];
static int g[12], used[12];
static int S[30][4];
static long long nodes = 0, witnesses = 0;
static int first_g[12];

static double mag(const int c[4]) {
    /* |c0 + c1*w + c2*w^2 + c3*w^3|, w = e^{i pi/6}: (1,0); w:(.866,.5); w^2:(.5,.866); w^3:(0,1) */
    double re = c[0] + 0.86602540378443865*c[1] + 0.5*c[2];
    double im = 0.5*c[1] + 0.86602540378443865*c[2] + 1.0*c[3];
    return sqrt(re*re + im*im);
}

static void dfs(int pos) {
    nodes++;
    if (pos == 12) {
        for (int c = 0; c < ncond; c++)
            if (S[c][0] || S[c][1] || S[c][2] || S[c][3]) return;
        witnesses++;
        if (witnesses == 1) memcpy(first_g, g, sizeof g);
        return;
    }
    for (int v = 0; v < 12; v++) {
        if (used[v]) continue;
        int a = g[pos-1], b = v;
        int ok = 1;
        for (int c = 0; c < ncond; c++) {
            int k = ((csig_p[c]*a - csig_q[c]*b) % 12 + 24) % 12;
            S[c][0] += ADD[k][0]; S[c][1] += ADD[k][1];
            S[c][2] += ADD[k][2]; S[c][3] += ADD[k][3];
        }
        if (pos < 11) {
            int remaining = 11 - pos;
            for (int c = 0; c < ncond && ok; c++)
                if (mag(S[c]) > remaining + 0.5) ok = 0;
        }
        if (ok) {
            used[v] = 1; g[pos] = v;
            dfs(pos + 1);
            used[v] = 0;
        }
        for (int c = 0; c < ncond; c++) {
            int k = ((csig_p[c]*a - csig_q[c]*b) % 12 + 24) % 12;
            S[c][0] -= ADD[k][0]; S[c][1] -= ADD[k][1];
            S[c][2] -= ADD[k][2]; S[c][3] -= ADD[k][3];
        }
    }
}

int main(int argc, char **argv) {
    const char *mode = (argc > 1) ? argv[1] : "full";
    if (strcmp(mode, "planar") == 0) {
        ncond = 1; csig_p[0] = 1; csig_q[0] = -1;   /* exponent = a + b */
    } else {
        ncond = 0;
        for (int i = 0; i < 6; i++)
            for (int j = 0; j < 6; j++)
                if (i != j) { csig_p[ncond] = SIG[i]; csig_q[ncond] = SIG[j]; ncond++; }
        /* 6*5 = 30 */
    }
    memset(S, 0, sizeof S); memset(used, 0, sizeof used);
    g[0] = 0; used[0] = 1;   /* fix global shift */
    dfs(1);
    printf("mode=%s ncond=%d nodes=%lld witnesses=%lld\n", mode, ncond, nodes, witnesses);
    if (witnesses > 0) {
        printf("first_witness_g:");
        for (int i = 0; i < 12; i++) printf(" %d", first_g[i]);
        printf("\n");
    }
    return 0;
}
