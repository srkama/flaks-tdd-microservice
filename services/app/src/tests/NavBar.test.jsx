import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme';
import { MemoryRouter as Router } from 'react-router-dom';
import renderer from 'react-test-renderer';
import NavBar from '../components/NavBar';

test('should render NavBar properly', () => {
    const wrapper = shallow(<NavBar title='Title' />);
    const element = wrapper.find('strong')
    expect(element.length).toBe(1);
    expect(element.get(0).props.children).toBe('Title');
});

test('should render NavBar snapshot properly', () => {
    const title = 'Test App';
    const tree = renderer.create(
        <Router location="/"><NavBar title={title} /></Router>
    ).toJSON()
    expect(tree).toMatchSnapshot();
});