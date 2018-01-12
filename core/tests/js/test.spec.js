describe('dit', function () {
  // Add the language selector to the page or language select js will error
  const html = '<section role="dialog" data-component="language-selector-dialog" data-lang="en" data-label="UK" data-name="English" class="language-selector-dialog"></section>';

  $('body').append(html);

  it('object should exist', function () {
    expect(dit).to.exist;
  });

  it('should have classes', function () {
    expect(dit.classes).to.have.property('Expander');
    expect(dit.classes).to.have.property('Accordion');
    expect(dit.classes).to.have.property('SelectTracker');
    expect(dit.classes).to.have.property('Modal');
  });

  it('should have components', function () {
    expect(dit.components).to.have.property('menu');
    expect(dit.components).to.have.property('languageSelector');
    expect(dit.components).to.have.property('video');
  });

  it('data should exist', function () {
    expect(dit.data).to.exist;
  });

  it('pages should have international', function () {
    expect(dit.pages).to.have.property('international');
  });

  it('constants should exist', function () {
    expect(dit.constants).to.exist;
  });

});
