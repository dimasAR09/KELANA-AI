describe('Kelana AI - E2E Testing (Live Production)', () => {

  it('Skenario 1: Navigasi Menu dari Beranda', () => {
    cy.visit('https://kelana-ai-henna.vercel.app/');
    
    cy.get('a[href="/login"]').should('be.visible').click();
    
    cy.url().should('include', '/login');
    
    cy.go('back');
  });

  it('Skenario 2: Mengirim Pesan ke AI Bedrock', () => {
    cy.visit('https://kelana-ai-henna.vercel.app/');
    
    cy.get('textarea').first().type('Halo Kelana, ini adalah pesan otomatis dari Cypress.');
    
    cy.get('button[type="submit"]').click();

    cy.get('textarea').first().should('have.value', '');

    cy.get('.balasan-ai, p', { timeout: 15000 })
      .should('be.visible'); 
  });

});