import React from 'react'
import { shallow } from 'enzyme';
import UserList from '../components/UserList';
import renderer from 'react-test-renderer';

const users = [
    { id: '1', 'username': 'kamal', 'email': 'kamal.s@gc.com' },
    { id: '2', 'username': 'kamal1', 'email': 'kamal1.s@gc.com' }]

test('UserLists renders proprely', () => {
    const wrapper = shallow(<UserList users={users} />);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('kamal');
    expect(element.get(1).props.children).toBe('kamal1');
})

test('Users snapshots renders properly', () => {
    const tree = renderer.create(<UserList users={users} />).toJSON();
    expect(tree).toMatchSnapshot();
})
