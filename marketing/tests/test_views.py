from unittest.mock import patch
from bs4 import BeautifulSoup
from django.urls import reverse

from core.tests.helpers import create_response


page_all_fields = {
    'campaign_heading': 'Campaign heading',
    'campaign_hero_image': {'url': 'campaign_hero_image.jpg'},
    'cta_box_button_text': 'CTA box button text',
    'cta_box_button_url': '/cta_box_button_url',
    'cta_box_message': 'CTA box message',
    'related_content_heading': 'Related content heading',
    'related_content_intro': '<p>Related content intro.</p>',
    'related_page_one_description': 'Related page one description',
    'related_page_one_heading': 'Related page one heading',
    'related_page_one_image': {'url': 'related_page_one_image.jpg'},
    'related_page_one_url': '/related_page_one_url',
    'related_page_two_description': 'Related page two description',
    'related_page_two_heading': 'Related page two heading',
    'related_page_two_image': {'url': 'related_page_two_image.jpg'},
    'related_page_two_url': '/related_page_two_url',
    'related_page_three_description': 'Related page three description',
    'related_page_three_heading': 'Related page three heading',
    'related_page_three_image': {'url': 'related_page_three_image.jpg'},
    'related_page_three_url': '/related_page_three_url',
    'section_one_contact_button_text': 'Section one contact button text',
    'section_one_contact_button_url': '/section_one_contact_button_url',
    'section_one_heading': 'Section one heading',
    'section_one_image': {'url': 'section_one_image.jpg'},
    'section_one_intro': '<p>Section one intro.</p>',
    'section_two_contact_button_text': 'Section one contact button text',
    'section_two_contact_button_url': '/section_two_contact_button_url',
    'section_two_heading': 'Section two heading',
    'section_two_image': {'url': 'section_two_image.jpg'},
    'section_two_intro': '<p>Section two intro</p>',
    'selling_point_one_content': '<p>Selling point one content</p>',
    'selling_point_one_heading': 'Selling point one heading',
    'selling_point_one_icon': {'url': 'selling_point_one_icon.jpg'},
    'selling_point_two_content': '<p>Selling point two content</p>',
    'selling_point_two_heading': 'Selling point two heading',
    'selling_point_two_icon': {'url': 'selling_point_two_icon.jpg'},
    'selling_point_three_content': '<p>Selling point three content</p>',
    'selling_point_three_heading': 'Selling point three heading',
    'selling_point_three_icon': {'url': 'selling_point_three_icon.jpg'},
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_marketing_campaign_page_all_fields(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON'] = True

    url = reverse('campaign-page', kwargs={'slug': 'test-page'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page_all_fields
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['marketing/campaign.html']

    soup = BeautifulSoup(response.content, 'html.parser')

    assert ('<p class="body-text">Selling point two content</p>'
            ) in str(response.content)

    assert ('<p class="body-text">Selling point three content</p>'
            ) in str(response.content)

    hero_section = soup.find(id='campaign-hero')

    exp_style = "background-image: url('{}')".format(
        page_all_fields['campaign_hero_image']['url'])

    assert hero_section.attrs['style'] == exp_style

    assert soup.find(
        id='selling-points-icon-two').attrs['src'] == page_all_fields[
        'selling_point_two_icon']['url']

    assert soup.find(
        id='selling-points-icon-three').attrs['src'] == page_all_fields[
        'selling_point_three_icon']['url']

    assert soup.find(
        id='section-one-contact-button').attrs['href'] == page_all_fields[
        'section_one_contact_button_url']
    assert soup.find(
        id='section-one-contact-button').text == page_all_fields[
        'section_one_contact_button_text']

    assert soup.find(
        id='section-two-contact-button').attrs['href'] == page_all_fields[
        'section_two_contact_button_url']
    assert soup.find(
        id='section-two-contact-button').text == page_all_fields[
        'section_two_contact_button_text']

    related_page_one = soup.find(id='related-page-one')
    assert related_page_one.find('a').text == page_all_fields[
        'related_page_one_heading']
    assert related_page_one.find('p').text == page_all_fields[
        'related_page_one_description']
    assert related_page_one.find('a').attrs['href'] == page_all_fields[
        'related_page_one_url']
    assert related_page_one.find('img').attrs['src'] == page_all_fields[
        'related_page_one_image']['url']

    related_page_two = soup.find(id='related-page-two')
    assert related_page_two.find('a').text == page_all_fields[
        'related_page_two_heading']
    assert related_page_two.find('p').text == page_all_fields[
        'related_page_two_description']
    assert related_page_two.find('a').attrs['href'] == page_all_fields[
        'related_page_two_url']
    assert related_page_two.find('img').attrs['src'] == page_all_fields[
        'related_page_two_image']['url']

    related_page_three = soup.find(id='related-page-three')
    assert related_page_three.find('a').text == page_all_fields[
        'related_page_three_heading']
    assert related_page_three.find('p').text == page_all_fields[
        'related_page_three_description']
    assert related_page_three.find('a').attrs['href'] == page_all_fields[
        'related_page_three_url']
    assert related_page_three.find('img').attrs['src'] == page_all_fields[
        'related_page_three_image']['url']

    assert soup.find(
        id='related-page-one-description').text == page_all_fields[
        'related_page_one_description']


page_required_fields = {
    'campaign_heading': 'Campaign heading',
    'campaign_hero_image': None,
    'cta_box_button_text': 'CTA box button text',
    'cta_box_button_url': '/cta_box_button_url',
    'cta_box_message': 'CTA box message',
    'related_content_heading': 'Related content heading',
    'related_content_intro': '<p>Related content intro.</p>',
    'related_page_one_description': None,
    'related_page_one_heading': None,
    'related_page_one_image': None,
    'related_page_one_url': None,
    'related_page_two_description': None,
    'related_page_two_heading': None,
    'related_page_two_image': None,
    'related_page_two_url': None,
    'related_page_three_description': None,
    'related_page_three_heading': None,
    'related_page_three_image': None,
    'related_page_three_url': None,
    'section_one_contact_button_text': None,
    'section_one_contact_button_url': None,
    'section_one_heading': 'Section one heading',
    'section_one_image': None,
    'section_one_intro': '<p>Section one intro.</p>',
    'section_two_contact_button_text': None,
    'section_two_contact_button_url': None,
    'section_two_heading': 'Section two heading',
    'section_two_image': None,
    'section_two_intro': '<p>Section two intro</p>',
    'selling_point_one_content': '<p>Selling point one content</p>',
    'selling_point_one_heading': 'Selling point one heading',
    'selling_point_one_icon': None,
    'selling_point_two_content': '<p>Selling point two content</p>',
    'selling_point_two_heading': 'Selling point two heading',
    'selling_point_two_icon': None,
    'selling_point_three_content': '<p>Selling point three content</p>',
    'selling_point_three_heading': 'Selling point three heading',
    'selling_point_three_icon': None,
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_marketing_campaign_page_required_fields(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON'] = True

    url = reverse('campaign-page', kwargs={'slug': 'test-page'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page_required_fields
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['marketing/campaign.html']

    soup = BeautifulSoup(response.content, 'html.parser')

    assert ('<p class="body-text">Selling point two content</p>'
            ) in str(response.content)

    assert ('<p class="body-text">Selling point three content</p>'
            ) in str(response.content)

    hero_section = soup.find(id='campaign-hero')
    assert not hero_section.attrs.get('style')

    assert not soup.find(id='selling-points-icon-two')
    assert not soup.find(id='selling-points-icon-three')

    assert not soup.find(id='section-one-contact-button')
    assert not soup.find(id='section-one-contact-button')

    assert not soup.find(id='section-two-contact-button')
    assert not soup.find(id='section-two-contact-button')

    assert soup.select(
        '#campaign-contact-box .box-heading'
        )[0].text == page_required_fields['cta_box_message']

    assert soup.find(
        id='campaign-hero-heading'
        ).text == page_required_fields['campaign_heading']

    assert soup.find(
        id='section-one-heading'
        ).text == page_required_fields['section_one_heading']

    assert soup.find(
        id='section-two-heading'
        ).text == page_required_fields['section_two_heading']

    assert soup.find(
        id='related-content-heading'
        ).text == page_required_fields['related_content_heading']

    assert soup.select(
        "li[aria-current='page']"
        )[0].text == page_required_fields['campaign_heading']
