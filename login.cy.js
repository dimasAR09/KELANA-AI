describe('Kelana AI - Fungsionalitas Login (Live Production)', () => {
  
  beforeEach(() => {
    cy.visit('https://kelana-ai-henna.vercel.app/login'); 
  });

  it('Berhasil Login dengan Akun Testing', () => {
    cy.get('input[type="email"]').type('akun.tester@kelana-ai.com');
    cy.get('input[type="password"]').type('TesterPassword123!');
    
    cy.get('button[type="submit"]').click();
    
    cy.url().should('not.include', '/login');
    
    cy.get('button').contains('Logout').should('exist');
  });

  it('Gagal Login dengan Password Salah', () => {
    cy.get('input[type="email"]').type('akun.tester@kelana-ai.com');
    cy.get('input[type="password"]').type('SalahPassword123!');
    
    cy.get('button[type="submit"]').click();
    
    cy.url().should('include', '/login');
  });
});