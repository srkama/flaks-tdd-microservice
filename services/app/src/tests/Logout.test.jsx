import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme';
import { MemoryRouter as Router } from 'react-router-dom';
import renderer from 'react-test-renderer';
import Logout from '../components/Logout';

const logoutUser = jest.fn();

test('Logout renders properly', () => {
    const wrapper = shallow(<Logout logout={logoutUser} />);
    const element = wrapper.find('p')
    expect(element.length).toBe(1);
    expect(element.get(0).props.children).toBe('You are logged out!');
})

test('Logout renders snapshot properly', () => {
    const tree = renderer.create(<Logout logout={logoutUser} />).toJSON();
    expect(tree).toMatchSnapshot();
})
